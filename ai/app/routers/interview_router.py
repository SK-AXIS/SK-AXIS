# app/routers/interview_router.py
from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
import httpx

from app.schemas.interview import (
    StartInterviewRequest,
    StartInterviewResponse,
    EndInterviewRequest,
    EndInterviewResponse,
    Question,
    NonverbalData
)

from app.services.pipeline.graph_pipeline import final_report_flow_executor, interview_flow_executor
from app.schemas.state import InterviewState
from app.state.store import INTERVIEW_STATE_STORE  # 전역 메모리 스토어
from app.services.interview.nonverbal_service import evaluate
from app.state.question_store import QUESTION_STORE

from app.services.interview.interview_end_processing_service import (
    process_last_audio_segment,
    save_nonverbal_counts
)

# 환경 변수 로드
load_dotenv()

router = APIRouter(prefix="/interview", tags=["Interview"])

RESULT_DIR = os.getenv("RESULT_DIR", "./result")
os.makedirs(RESULT_DIR, exist_ok=True)

SPRINGBOOT_BASE_URL = os.getenv("SPRING_API_URL", "http://localhost:8080/api/v1")

@router.post("/start", response_model=StartInterviewResponse)
async def start_interview(req: StartInterviewRequest):
    url = f"{SPRINGBOOT_BASE_URL}/interviews/start"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"interviewee_ids": req.interviewee_ids})
        if response.status_code == 200:
            questions_per_interviewee = response.json().get("questions_per_interviewee", {})
            if not questions_per_interviewee:
                raise HTTPException(status_code=404, detail="질문을 찾을 수 없습니다.")
            for interviewee_id, questions in questions_per_interviewee.items():
                QUESTION_STORE[int(interviewee_id)] = questions
            return StartInterviewResponse(questions_per_interviewee=questions_per_interviewee)
        else:
            raise HTTPException(status_code=response.status_code, detail="질문을 찾을 수 없습니다.")

@router.post("/end", response_model=EndInterviewResponse)
async def end_interview(req: EndInterviewRequest):
    """Swagger 명세에 맞춘 Map 구조 처리"""
    processed_count = 0
    skipped_ids = []

    try:
        for interviewee_id_str, nv in req.data.items():
            interviewee_id = int(interviewee_id_str)
            print(f"[DEBUG] Processing interviewee_id: {interviewee_id}")

            # state가 없는 경우 스킵
            state: InterviewState = INTERVIEW_STATE_STORE.get(interviewee_id)
            print(f"[TRACE] INTERVIEW_STATE_STORE 조회: interviewee_id={interviewee_id}, state type={type(state)}, value={state}")
            if not state:
                # print(f"[INFO] Skipping interviewee {interviewee_id} - No state found")
                skipped_ids.append(interviewee_id)
                continue
            if not isinstance(state, dict):
                print(f"[ERROR] [INTERVIEW_ROUTER] state가 dict가 아님! interviewee_id={interviewee_id}, 실제 타입: {type(state)}, 값: {state}")
                skipped_ids.append(interviewee_id)
                continue

            if not isinstance(nv, NonverbalData):
                # print("[DEBUG] NonverbalData로 변환 시도")
                nv = NonverbalData(**nv)
            # print(f"[DEBUG] 변환된 nv 데이터: {nv}")

            # (1) 마지막 녹음 파일 처리
            if state.get("audio_path"):
                state = await interview_flow_executor.ainvoke(state, config={"recursion_limit": 10})
                state["audio_path"] = ""  # 중복 실행 방지

            # (2) 비언어적 카운트 저장 — 에이전트에서는 facial_expression 키만 봅니다.
            state["nonverbal_counts"] = {
                "facial_expression": nv.facial_expression.dict()
            }
            # (선택) 타임스탬프가 필요하다면 별도 필드에 저장
            state["nonverbal_meta"] = {"timestamp": nv.timestamp}

            print(f"[DEBUG] state['nonverbal_counts']: {state['nonverbal_counts']}")

            # (3) 최종 리포트 생성
            state = await final_report_flow_executor.ainvoke(state, config={"recursion_limit": 10})
            processed_count += 1

        if processed_count == 0:
            print("[WARNING] No interviewees were processed")
            return EndInterviewResponse(
                result="partial",
                report_ready=False,
                message=f"No states found for any interviewees. Skipped IDs: {skipped_ids}"
            )

        return EndInterviewResponse(
            result="done" if len(skipped_ids) == 0 else "partial",
            report_ready=True,
            message=None if len(skipped_ids) == 0 else f"Skipped interviewees: {skipped_ids}"
        )

    except Exception as e:
        print(f"[DEBUG] Exception: {e}")
        from app.state.store import debug_dump_state_store
        debug_dump_state_store()
        # state 내부 구조 추가 진단
        try:
            if 'state' in locals() and isinstance(state, dict):
                # print("[DIAG] state 내부 주요 필드 타입 및 값:")
                for field in ["audio_path", "stt", "rewrite", "evaluation", "report", "decision_log", "nonverbal_counts"]:
                    v = state.get(field, "<없음>")
                    print(f"  {field}: type={type(v)}, value={v}")
        except Exception as diag_e:
            print(f"[DIAG] state 내부 구조 출력 중 오류: {diag_e}")
        raise HTTPException(status_code=500, detail=str(e))
