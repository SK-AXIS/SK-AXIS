# app/services/pipeline/pipeline_agents.py

from datetime import datetime
import json
from app.schemas.state import InterviewState
from app.schemas.nonverbal import FacialExpression
from app.services.interview.rewrite_service import rewrite_answer
from app.services.interview.evaluation_service import evaluate_keywords_from_full_answer
from app.services.interview.nonverbal_service import evaluate
from app.constants.evaluation_constants_full_all import (
    EVAL_CRITERIA_WITH_ALL_SCORES,
    TECHNICAL_EVAL_CRITERIA_WITH_ALL_SCORES,
    DOMAIN_EVAL_CRITERIA_WITH_ALL_SCORES
)
from .pipeline_chains import chains
from .pipeline_utils import utils, KST

async def rewrite_agent(state: InterviewState) -> InterviewState:
    """
    STT 결과를 문법적으로 정제하는 리라이팅 에이전트
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        InterviewState: 리라이팅 결과가 추가된 상태
        
    처리 과정:
    1. STT 결과에서 마지막 세그먼트 추출
    2. GPT-4o-mini로 의미 보존 기반 텍스트 정제
    3. 재시도 횟수 관리 (현재 재시도 비활성화)
    4. 결과를 state["rewrite"]["items"]에 저장
    
    Note:
        - 지원자 답변 의미 절대 변경 안 함
        - 문법 오류 및 불필요한 공백 제거
        - 면접관 발언 필터링
        - GPT-4o-mini 사용으로 비용 절약
    """
    print("[LangGraph] ✏️ rewrite_agent 진입")
    stt = utils.safe_get(state, "stt", {}, context="rewrite_agent")
    stt_segments = utils.safe_get(stt, "segments", [], context="rewrite_agent")
    
    if not stt_segments:
        print("[LangGraph] ⚠️ STT 세그먼트가 없음")
        return state
    
    # 마지막 STT 세그먼트 확인
    last_segment = stt_segments[-1]
    raw = last_segment.get("raw", "없음")
    
    # 무의미한 STT 결과인지 확인
    if last_segment.get("meaningless", False):
        print(f"[LangGraph] 🚫 무의미한 STT 결과 - 리라이팅 건너뜀: {raw}")
        utils.add_decision_log(state, "rewrite_agent", "skipped", {
            "reason": "meaningless_stt_result",
            "raw": raw
        })
        return state
    
    if not raw or not str(raw).strip():
        raw = "없음"
    
    rewritten, _ = await rewrite_answer(raw)
    if not rewritten or not str(rewritten).strip():
        rewritten = "없음"
    item = {"raw": raw, "rewritten": rewritten}

    prev = utils.safe_get(state, "rewrite", {}, context="rewrite_agent")
    prev_retry = utils.safe_get(prev, "retry_count", 0, context="rewrite_agent")
    prev_force = utils.safe_get(prev, "force_ok", False, context="rewrite_agent")
    prev_final = utils.safe_get(prev, "final", [], context="rewrite_agent")

    # retry_count가 3 이상이면 더 이상 증가시키지 않음
    if prev_retry >= 3:
        retry_count = 3
        force = True
    else:
        retry_count = prev_retry + 1
        force = prev_force

    state["rewrite"] = {
        **prev,
        "done": False,
        "items": prev.get("items", []) + [item],
        "retry_count": retry_count,
        "force_ok": force,
        "final": prev_final
    }

    utils.add_decision_log(state, "rewrite_agent", "done", {
        "retry_count": retry_count,
        "force": force
    })

    return state

async def rewrite_judge_agent(state: InterviewState) -> InterviewState:
    """
    리라이팅 결과를 검증하는 판정 에이전트
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        InterviewState: 검증 결과가 추가된 상태
        
    처리 과정:
    1. 리라이팅 결과 품질 검증 (의미 보존, 문법 정확성)
    2. GPT-4o-mini로 판정 수행
    3. 검증 통과 시 final 배열에 추가
    4. 강제 통과 플래그 처리
    
    Note:
        - 현재 재시도 로직 비활성화로 대부분 통과
        - JSON 파싱 오류 시 안전 처리
        - 중복 답변 필터링 로직 포함
    """
    print("[LangGraph] 🧪 rewrite_judge_agent 진입")
    rewrite = utils.safe_get(state, "rewrite", {}, context="rewrite_judge_agent")
    items   = utils.safe_get(rewrite, "items", [])
    force   = utils.safe_get(rewrite, "force_ok", False, context="rewrite_judge_agent")

    if not items:
        utils.add_decision_log(state, "rewrite_judge_agent", "error", {
            "error": "No rewrite items found"
        })
        return state

    for item in items:
        if "ok" in item:
            continue

        try:
            # 체이닝 사용
            result = await chains.rewrite_judge_chain.ainvoke({
                "raw": item["raw"],
                "rewritten": item["rewritten"]
            })
            
            item["ok"] = result.get("ok", False)
            item["judge_notes"] = result.get("judge_notes", [])

            print(f"[DEBUG] 📊 판정 결과: ok={item['ok']}, notes={item['judge_notes']}")

            # 강제 통과 플래그 처리
            if not item["ok"] and force:
                print("⚠️ rewrite 실패 항목 강제 ok 처리됨")
                item["ok"] = True
                item["judge_notes"].append("강제 통과 (재시도 3회 초과)")

            if item["ok"]:
                # 중복된 rewritten 답변이 이미 final에 있으면 추가하지 않음
                rewritten = item["rewritten"]
                if not any(f["rewritten"] == rewritten for f in rewrite.get("final", [])):
                    rewrite.setdefault("final", []).append({
                        "raw":       item["raw"],
                        "rewritten": rewritten,
                        "timestamp": datetime.now(KST).isoformat()
                    })
                else:
                    pass

            # 강제 통과 플래그가 설정되어 있으면 final에 추가
            if force and not item.get("ok", False):
                print("⚠️ 강제 통과 플래그로 인해 final에 추가")
                rewritten = item["rewritten"]
                if not any(f["rewritten"] == rewritten for f in rewrite.get("final", [])):
                    rewrite.setdefault("final", []).append({
                        "raw":       item["raw"],
                        "rewritten": rewritten,
                        "timestamp": datetime.now(KST).isoformat()
                    })
                else:
                    pass
                item["ok"] = True
                item["judge_notes"].append("강제 통과 (재시도 3회 초과)")

            utils.add_decision_log(state, "rewrite_judge_agent", f"ok={item['ok']}", {
                "notes": item["judge_notes"]
            })
            print(f"[LangGraph] ✅ 판정 결과: ok={item['ok']}")

        except Exception as e:
            print(f"[ERROR] rewrite_judge_agent 체인 실행 오류: {e}")
            item["ok"] = False
            item["judge_notes"] = [f"judge error: {e}"]
            utils.add_decision_log(state, "rewrite_judge_agent", "error", {
                "error": str(e)
            })

    # 마지막 항목이 ok=True면 완료 표시
    if rewrite["items"][-1].get("ok", False):
        rewrite["done"] = True
    return state

async def nonverbal_evaluation_agent(state: InterviewState) -> InterviewState:
    """
    비언어적 요소(표정)를 평가하는 에이전트
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        InterviewState: 비언어적 평가 결과가 추가된 상태
        
    처리 과정:
    1. nonverbal_counts에서 표정 데이터 추출
    2. FacialExpression 객체로 변환
    3. GPT-4o-mini로 표정 패턴 분석
    4. 0.0~1.0 점수를 15점 만점으로 환산
    5. 결과를 state["evaluation"]["results"]["비언어적"]에 저장
    
    Note:
        - 프론트엔드에서 수집된 smile, neutral, frown, angry 횟수 기반
        - 적절한 표정 변화와 웃음은 긍정적 평가
        - 데이터 누락 시 경고 메시지 출력
    """
    # 평가 시작 시간 기록
    evaluation_start_time = datetime.now(KST).timestamp()
    state["_evaluation_start_time"] = evaluation_start_time
    print(f"[⏱️] 평가 시작: {datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')}")
    
    ts = datetime.now(KST).isoformat()
    try:
        counts = utils.safe_get(state, "nonverbal_counts", {}, context="nonverbal_evaluation_agent")
        print(f"[DEBUG] nonverbal_counts: {counts}")
        # 구조 체크
        if not counts or not isinstance(counts, dict):
            print("[WARNING] nonverbal_counts가 dict가 아님 또는 비어있음. 비언어적 평가를 건너뜀.")
            state.decision_log.append("Nonverbal data not available for evaluation.")
            return state
        if "expression" not in counts or not isinstance(counts["expression"], dict):
            print("[WARNING] nonverbal_counts['expression']가 dict가 아님 또는 없음. 비언어적 평가를 건너뜀.")
            state.decision_log.append("Nonverbal expression data not available for evaluation.")
            return state
        # expression 내부 키 체크
        exp = counts["expression"]
        required_keys = ["smile", "neutral", "frown", "angry"]
        for k in required_keys:
            if k not in exp or not isinstance(exp[k], int):
                print(f"[WARNING] nonverbal_counts['expression']에 {k}가 없거나 int가 아님: {exp}")
        facial = FacialExpression.parse_obj(exp)
        print(f"[DEBUG] facial_expression: {facial}")
        res = await evaluate(facial)
        score = res.get("score", 0)
        analysis = res.get("analysis", "")
        feedback = res.get("feedback", "")
        # print(f"[DEBUG] 비언어적 평가 결과(score): {score}, analysis: {analysis}, feedback: {feedback}")
        pts = int(round(score * 15))
        if pts == 0:
            print("[WARNING] 비언어적 평가 점수가 0입니다. 프론트/데이터 전달/LLM 프롬프트를 확인하세요.")
        evaluation = utils.safe_get(state, "evaluation", {}, context="nonverbal_evaluation_agent")
        results = utils.safe_get(evaluation, "results", {}, context="nonverbal_evaluation_agent")
        results["비언어적"] = {"score": pts, "reason": analysis or feedback or "평가 사유없음"}
        state.setdefault("evaluation", {}).setdefault("results", {})["비언어적"] = {
            "score": pts,
            "reason": analysis or feedback or "평가 사유없음"
        }
        utils.add_decision_log(state, "nonverbal_evaluation", "success", {
            "score": pts
        })
        print(f"[DEBUG] nonverbal_evaluation_agent - state['evaluation']['results']['비언어적']: {state.get('evaluation', {}).get('results', {}).get('비언어적')}")
    except Exception as e:
        print(f"[ERROR] 비언어적 평가 중 예외 발생: {e}")
        utils.add_decision_log(state, "nonverbal_evaluation", "error", {
            "error": str(e)
        })
    return state

async def evaluation_agent(state: InterviewState) -> InterviewState:
    """
    키워드별 평가를 수행하는 에이전트
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        InterviewState: 평가 결과가 추가된 상태
        
    처리 과정:
    1. 리라이팅된 답변들을 하나의 텍스트로 결합
    2. 8개 키워드 × 3개 기준 = 24개 항목 평가
    3. 평가 결과 정규화 및 병합
    4. 재시도 횟수 관리
    
    Note:
        - GPT-4o-mini 사용으로 비용 절약
        - 평가 결과 정규화로 일관성 확보
        - 비언어적 평가 결과와 병합
    """
    print("[LangGraph] 🧠 evaluation_agent 진입")
    
    # 리라이팅된 답변들을 하나의 텍스트로 결합
    rewrite = utils.safe_get(state, "rewrite", {}, context="evaluation_agent:rewrite")
    final_items = utils.safe_get(rewrite, "final", [], context="evaluation_agent:rewrite.final")
    
    if not final_items:
        print("[WARNING] final_items가 비어있음. 평가를 건너뜀.")
        utils.add_decision_log(state, "evaluation_agent", "error", {
            "error": "No final items found"
        })
        return state
    
    full_answer = "\n".join(item["rewritten"] for item in final_items)
    print(f"[DEBUG] 평가 대상 답변: {full_answer[:100]}...")

    # 평가 기준 키 목록을 가져옴
    all_criteria = {**EVAL_CRITERIA_WITH_ALL_SCORES, **TECHNICAL_EVAL_CRITERIA_WITH_ALL_SCORES, **DOMAIN_EVAL_CRITERIA_WITH_ALL_SCORES}

    # 평가 결과를 정제하는 함수 (quotes 필드까지 보장)
    def normalize_results(results):
        normalized = {}
        for keyword, criteria in all_criteria.items():
            kw_result = results.get(keyword, {}) if isinstance(results, dict) else {}
            normalized[keyword] = {}
            for crit_name in criteria.keys():
                val = kw_result.get(crit_name) if isinstance(kw_result, dict) else None
                # 보강: dict가 아니면 무조건 dict로 감싸기
                if not isinstance(val, dict):
                    if isinstance(val, int):
                        val = {"score": val, "reason": "평가 사유없음", "quotes": []}
                    else:
                        val = {"score": 1, "reason": "평가 사유없음", "quotes": []}
                score = val.get("score", 1)
                reason = val.get("reason", "평가 사유없음")
                quotes = val.get("quotes", [])
                if not isinstance(quotes, list):
                    quotes = []
                normalized[keyword][crit_name] = {
                    "score": score,
                    "reason": reason,
                    "quotes": quotes
                }
        # 비언어적 요소도 항상 dict로 보정
        if "비언어적" in results:
            nonverbal = results["비언어적"]
            if not isinstance(nonverbal, dict):
                if isinstance(nonverbal, int):
                    nonverbal = {"score": nonverbal, "reason": "평가 사유없음", "quotes": []}
                else:
                    nonverbal = {"score": 1, "reason": "평가 사유없음", "quotes": []}
            if "quotes" not in nonverbal or not isinstance(nonverbal["quotes"], list):
                nonverbal["quotes"] = []
            normalized["비언어적"] = nonverbal
        return normalized

    results = await evaluate_keywords_from_full_answer(full_answer)
    results = normalize_results(results)

    prev_eval = utils.safe_get(state, "evaluation", {}, context="evaluation_agent:evaluation")
    prev_results = prev_eval.get("results", {})
    # 기존 비언어적 등 결과와 새 평가 결과 병합
    merged_results = {**prev_results, **results}
    prev_retry = utils.safe_get(prev_eval, "retry_count", 0, context="evaluation_agent:evaluation.retry_count")
    if "ok" in prev_eval and utils.safe_get(prev_eval, "ok", context="evaluation_agent:evaluation.ok") is False:
        retry_count = prev_retry + 1
    else:
        retry_count = prev_retry

    state["evaluation"] = {
        **prev_eval,
        "done": True,
        "results": merged_results,
        "retry_count": retry_count,
        "ok": False  # 판정 전이므로 False로 초기화
    }
    state["done"] = True  # 파이프라인 전체 종료 신호 추가
    utils.add_decision_log(state, "evaluation_agent", "done", {
        "retry_count": retry_count
    })

    return state

async def evaluation_judge_agent(state: InterviewState) -> InterviewState:
    """
    평가 결과를 검증하는 판정 에이전트
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        InterviewState: 검증 결과가 추가된 상태
        
    검증 항목:
    1. 구조적 검증: 각 키워드당 3개 기준 존재 여부
    2. 점수 범위 검증: 1~5점 범위 내 점수 확인
    3. 총점 검증: 최대 점수 초과 여부 확인
    4. 내용 검증: GPT-4o-mini로 평가 내용 타당성 검증
    
    Note:
        - 검증 실패 시에도 재시도 제한으로 진행
        - 내용 검증 오류 시 기본 통과 처리
        - 모든 검증 결과를 decision_log에 기록
    """
    evaluation = utils.safe_get(state, "evaluation", {}, context="evaluation_judge_agent:evaluation")
    results = utils.safe_get(evaluation, "results", {}, context="evaluation_judge_agent:evaluation.results")
    if not results:
        utils.add_decision_log(state, "evaluation_judge_agent", "error", {
            "error": "No evaluation results found"
        })
        print("[judge] No evaluation results found, will stop.")
        state["evaluation"]["ok"] = True  # 더 이상 retry/continue 안 하도록 True로 설정
        return state

    judge_notes = []
    is_valid = True

    # 1. 항목 수 검증 (각 키워드에 3개)
    for kw, criteria in results.items():
        if len(criteria) != 3:
            judge_notes.append(f"Keyword '{kw}' has {len(criteria)} criteria (expected 3)")
            is_valid = False

    # 2. 점수 범위 검증 (1~5)
    for criteria in results.values():
        for data in criteria.values():
            # print(f"[DEBUG] evaluation_judge_agent - data type: {type(data)}, value: {data}")
            if isinstance(data, dict):
                s = data.get("score", 0)
            elif isinstance(data, int):
                s = data
            else:
                s = 0
            if not (1 <= s <= 5):
                judge_notes.append(f"Invalid score {s}")
                is_valid = False

    # 3. 총점 검증
    total = 0
    for crit in results.values():
        for c in crit.values():
            if isinstance(c, dict):
                total += c.get("score", 0)
            elif isinstance(c, int):
                total += c
            else:
                total += 0
    max_score = len(results) * 3 * 5
    if total > max_score:
        judge_notes.append(f"Total {total} exceeds max {max_score}")
        is_valid = False

    print(f"[judge] is_valid={is_valid}, judge_notes={judge_notes}, total={total}, max_score={max_score}")
    state["evaluation"]["judge"] = {
        "ok": is_valid,
        "judge_notes": judge_notes,
        "total_score": total,
        "max_score": max_score
    }
    state["evaluation"]["ok"] = is_valid

    # === 내용 검증 LLM 호출 추가 ===
    try:
        final_items = utils.safe_get(state, "rewrite", {}).get("final", [])
        if not final_items:
            # final_items가 비어있으면 raw 텍스트 사용
            stt_segments = state.get("stt", {}).get("segments", [])
            if stt_segments:
                answer = stt_segments[-1].get("raw", "답변 내용이 없습니다.")
            else:
                answer = "답변 내용이 없습니다."
        else:
            answer = "\n".join(item["rewritten"] for item in final_items)
            
        evaluation = json.dumps(state.get("evaluation", {}).get("results", {}), ensure_ascii=False)
        criteria = json.dumps({
            **EVAL_CRITERIA_WITH_ALL_SCORES,
            **TECHNICAL_EVAL_CRITERIA_WITH_ALL_SCORES,
            **DOMAIN_EVAL_CRITERIA_WITH_ALL_SCORES
        }, ensure_ascii=False)

        # 체이닝 사용
        result = await chains.content_validation_chain.ainvoke({
            "answer": answer,
            "evaluation": evaluation,
            "criteria": criteria
        })
        
        state["evaluation"]["content_judge"] = {
            "ok": result.get("ok", False),
            "judge_notes": result.get("judge_notes", [])
        }
        print(f"[LangGraph] ✅ 내용 검증 결과: ok={result.get('ok', False)}, notes={result.get('judge_notes', [])}")
    except Exception as e:
        print(f"[ERROR] content_validation_chain 실행 오류: {e}")
        state["evaluation"]["content_judge"] = {
            "ok": True,  # 오류 시 기본적으로 통과
            "judge_notes": [f"content judge error: {e}"]
        }
        print(f"[LangGraph] ❌ 내용 검증 오류: {e}")

    utils.add_decision_log(state, "evaluation_judge_agent", f"ok={is_valid}", {
        "total_score": total,
        "max_score": max_score,
        "notes": judge_notes
    })
    
    return state

async def score_summary_agent(state: InterviewState) -> InterviewState:
    """
    평가 검증 후 최종 점수 환산 및 요약을 담당하는 에이전트
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        InterviewState: 최종 요약이 추가된 상태
        
    처리 과정:
    1. 영역별 점수 계산 및 100점 만점 환산
    2. 지원자 답변과 평가 사유를 GPT-4o로 종합 요약
    3. 평가 소요시간 계산 및 기록
    4. done 플래그 설정으로 파이프라인 완료
    
    최종 결과:
    - 인성적 요소: 45% (90점 → 45점)
    - 직무/도메인: 45% (30점 → 45점)  
    - 비언어적 요소: 10% (15점 → 10점)
    - 총점: 100점 만점
    
    Note:
        - GPT-4o 사용으로 고품질 요약 생성
        - 평가 소요시간 추적 및 성능 모니터링
        - 모든 결과를 state["summary"]에 저장
    """
    evaluation = utils.safe_get(state, "evaluation", {}, context="score_summary_agent:evaluation")
    evaluation_results = utils.safe_get(evaluation, "results", {}, context="score_summary_agent:evaluation.results")
    # print(f"[DEBUG] 평가 결과(evaluation_results): {json.dumps(evaluation_results, ensure_ascii=False, indent=2)}")
    nonverbal = evaluation_results.get("비언어적", {})
    nonverbal_score = nonverbal.get("score", 0)
    nonverbal_reason = nonverbal.get("reason", "평가 사유없음")
    # print(f"[DEBUG] 비언어적 평가: score={nonverbal_score}, reason={nonverbal_reason}")

    # 100점 만점 환산 점수 계산
    weights, personality_score_scaled, job_domain_score_scaled, nonverbal_score_scaled = utils.calculate_area_scores(evaluation_results, nonverbal_score)
    verbal_score = personality_score_scaled + job_domain_score_scaled
    # print(f"[DEBUG] verbal_score(인성+직무/도메인): {verbal_score}")

    # 전체 키워드 평가 사유 종합 (SUPEX, VWBE, Passionate, Proactive, Professional, People, 기술/직무, 도메인 전문성)
    all_keywords = [
        "SUPEX", "VWBE", "Passionate", "Proactive", "Professional", "People",
        "기술/직무", "도메인 전문성"
    ]
    reasons = []
    for keyword in all_keywords:
        for crit_name, crit in evaluation_results.items():
            reason = crit.get("reason", "")
            if reason:
                reasons.append(f"{keyword} - {crit_name}: {reason}")
            # print(f"[DEBUG] 평가 사유 추출: {keyword} - {crit_name} - {reason}")
    all_reasons = "\n".join(reasons)
    # print(f"[DEBUG] all_reasons(전체 평가 사유):\n{all_reasons}")

    # 지원자 답변 추출
    rewrite = utils.safe_get(state, "rewrite", {}, context="score_summary_agent:rewrite")
    final_items = utils.safe_get(rewrite, "final", [], context="score_summary_agent:rewrite.final")
    if final_items:
        answer = "\n".join(item["rewritten"] for item in final_items)
    else:
        stt = utils.safe_get(state, "stt", {}, context="score_summary_agent:stt")
        stt_segments = utils.safe_get(stt, "segments", [], context="score_summary_agent:stt.segments")
        if stt_segments:
            answer = "\n".join(seg.get("raw", "답변 내용이 없습니다.") for seg in stt_segments)
        else:
            answer = "답변 내용이 없습니다."
    # print(f"[DEBUG] 지원자 답변(answer):\n{answer}")

    # 체이닝 사용하여 요약 생성
    try:
        summary_response = await chains.score_summary_chain.ainvoke({
            "answer": answer,
            "all_reasons": all_reasons
        })
        verbal_reason = summary_response.strip().splitlines()[:8]
        # print(f"[DEBUG] summary_text(LLM 요약): {verbal_reason}")
    except Exception as e:
        print(f"[ERROR] score_summary_chain 실행 오류: {e}")
        verbal_reason = ["요약 생성 중 오류가 발생했습니다."]

    # 각 키워드별 총점 계산
    keyword_scores = {}
    for keyword, criteria in evaluation_results.items():
        if keyword == "비언어적":
            continue
        total = 0
        for crit in criteria.values():
            if isinstance(crit, dict):
                total += crit.get("score", 0)
            elif isinstance(crit, int):
                total += crit
        keyword_scores[keyword] = total

    # state에 저장
    state["summary"] = {
        "weights": weights,
        "personality_score": personality_score_scaled,
        "job_domain_score": job_domain_score_scaled,
        "verbal_score": verbal_score,
        "verbal_reason": verbal_reason,
        "nonverbal_score": nonverbal_score_scaled,
        "nonverbal_reason": nonverbal_reason,
        "keyword_scores": keyword_scores,
        "total_score": round(verbal_score + nonverbal_score_scaled, 1)
    }
    print(f"[LangGraph] ✅ 영역별 점수/요약 저장: {json.dumps(state['summary'], ensure_ascii=False, indent=2)}")

    # 평가 소요시간 계산 및 출력
    start_time = state.get("_evaluation_start_time")
    if start_time:
        end_time = datetime.now(KST).timestamp()
        total_elapsed = end_time - start_time
        print(f"[⏱️] 평가 완료: {datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[⏱️] 평가 소요시간: {total_elapsed:.2f}초 (평가 시작 → 완료)")
        
        # decision_log에도 기록
        utils.add_decision_log(state, "evaluation_complete", "success", {
            "evaluation_elapsed_seconds": round(total_elapsed, 2),
            "start_time": datetime.fromtimestamp(start_time, KST).isoformat(),
            "end_time": datetime.now(KST).isoformat()
        })
        
        # summary에도 소요시간 정보 추가
        state["summary"]["evaluation_duration"] = {
            "total_seconds": round(total_elapsed, 2),
            "start_time": datetime.fromtimestamp(start_time, KST).isoformat(),
            "end_time": datetime.now(KST).isoformat()
        }
    else:
        print("[⏱️] 평가 시작 시간 정보가 없습니다.")

    # 모든 처리 완료 - done 플래그 설정
    state["done"] = True
    print(f"[LangGraph] ✅ 모든 평가 완료 - done 플래그 설정")

    return state 