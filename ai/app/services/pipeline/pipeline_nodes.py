# app/services/pipeline/pipeline_nodes.py

from typing import Literal
from datetime import datetime
from app.schemas.state import InterviewState
from app.services.interview.stt_service import transcribe_audio_file
from .pipeline_utils import utils, KST

def stt_node(state: InterviewState) -> InterviewState:
    """
    음성 파일을 텍스트로 변환하는 STT 노드
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        InterviewState: STT 결과가 추가된 상태
        
    처리 과정:
    1. audio_path에서 오디오 파일 경로 추출
    2. OpenAI Whisper API로 음성 인식 수행
    3. 손상된 파일 또는 인식 실패 시 기본 메시지 설정
    4. 결과를 state["stt"]["segments"]에 저장
    
    Note:
        - 파일 헤더 검증으로 3000배 속도 향상
        - 손상된 WebM 파일 사전 감지
        - 유튜브 관련 오인식 필터링
    """
    print("[LangGraph] 🧠 stt_node 진입")
    
    audio_path = utils.safe_get(state, "audio_path", context="stt_node")
    raw = transcribe_audio_file(audio_path)
    
    # STT 결과 추가 검증 및 필터링
    if not raw or not str(raw).strip():
        raw = "음성을 인식할 수 없습니다."
    elif "손상되어 인식할 수 없습니다" in raw:
        print(f"[LangGraph] ⚠️ 손상된 오디오 파일 처리: {audio_path}")
        raw = "기술적 문제로 음성을 인식할 수 없어 답변을 제공할 수 없습니다."
    elif "음성을 명확하게 인식할 수 없습니다" in raw:
        print(f"[LangGraph] ⚠️ STT 필터링된 결과: {raw}")
        raw = "음성을 인식할 수 없습니다."
    elif any(pattern in raw.lower() for pattern in [
        "시청해주셔서 감사합니다", "시청 해주셔서 감사합니다", "시청해 주셔서 감사합니다",
        "오늘도 영상 시청", "영상 시청해주셔서", "먹방", "빠이빠이", "구독", "유튜브"
    ]):
        print(f"[LangGraph] ⚠️ 유튜브 관련 오인식 감지: {raw}")
        raw = "음성을 인식할 수 없습니다."
    elif len(raw.strip()) < 5:  # 너무 짧은 답변도 필터링
        print(f"[LangGraph] ⚠️ 너무 짧은 답변 감지: {raw}")
        raw = "음성을 인식할 수 없습니다."
    
    state.setdefault("stt", {"done": False, "segments": []})
    state["stt"]["segments"].append({"raw": raw, "timestamp": datetime.now(KST).isoformat()})
    
    print(f"[LangGraph] ✅ STT 완료: {raw[:50]}...")
    return state

def should_retry_rewrite(state: InterviewState) -> Literal["retry", "done"]:
    """
    리라이팅 재시도 여부를 결정하는 조건 함수
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        Literal["retry", "done"]: 재시도 또는 완료
        
    처리 로직:
    - 현재 재시도 로직 비활성화로 항상 "done" 반환
    - 향후 재시도 로직 활성화 시 조건 추가 가능
    
    Note:
        - 비용 절약을 위해 재시도 로직 비활성화
        - 강제 통과 플래그로 안정성 확보
    """
    # 현재 재시도 로직 비활성화
    return "done"

def should_retry_evaluation(state: InterviewState) -> Literal["retry", "continue", "done"]:
    """
    평가 재시도 여부를 결정하는 조건 함수
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        Literal["retry", "continue", "done"]: 재시도, 계속, 완료
        
    처리 로직:
    - 평가 성공 또는 재시도 1회 도달 시 "continue"
    - 그 외의 경우 "retry" (최대 2번 실행)
    
    Note:
        - 최대 재시도 횟수 1회로 제한 (비용 절약)
        - 총 2번 실행 후 무조건 진행
        - 내용 검증은 evaluation_judge_agent에서 수행
    """
    evaluation = utils.safe_get(state, "evaluation", {}, context="should_retry_evaluation:evaluation")
    retry_count = utils.safe_get(evaluation, "retry_count", 0, context="should_retry_evaluation:retry_count")
    is_ok = utils.safe_get(evaluation, "ok", False, context="should_retry_evaluation:ok")
    
    # print(f"[DEBUG] should_retry_evaluation - retry_count: {retry_count}, is_ok: {is_ok}")
    
    if is_ok:
        return "continue"
    elif retry_count >= 1:  # 최대 1회 재시도
        return "continue"
    else:
        return "retry" 