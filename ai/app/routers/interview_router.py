# app/routers/interview_router.py

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import os
from dotenv import load_dotenv

from app.schemas.interview import (
    StartInterviewRequest,
    StartInterviewResponse,
    EndInterviewRequest,
    EndInterviewResponse,
    STTUploadResponse
)
from app.services.internal_client import fetch_interviewee_questions
from app.services.pipeline.graph_pipeline import final_report_flow_executor, interview_flow_executor
from app.schemas.state import InterviewState
from app.state.store import INTERVIEW_STATE_STORE  # 전역 메모리 스토어
from app.services.interview.nonverbal_service import evaluate
from app.services.interview.stt_service import save_audio_file
from app.state.question_store import QUESTION_STORE
from app.services.interview.state_service import create_initial_state
from app.services.interview.interview_end_processing_service import (
    process_last_audio_segment,
    save_nonverbal_counts
)

# 환경 변수 로드
load_dotenv()

router = APIRouter(prefix="/interview", tags=["Interview"])

RESULT_DIR = os.getenv("RESULT_DIR", "./result")
os.makedirs(RESULT_DIR, exist_ok=True)


@router.post("/start", response_model=StartInterviewResponse)
async def start_interview(req: StartInterviewRequest):
    """
    인터뷰 시작: 각 지원자의 질문 목록을 로드해 반환하고,
    질문은 QUESTION_STORE에 저장합니다.
    """
    questions_per_interviewee = {}

    for interviewee_id in req.interviewee_ids:
        questions = await fetch_interviewee_questions(interviewee_id)
        if not questions:
            raise HTTPException(status_code=404, detail=f"{interviewee_id} 질문 없음")
        
        questions_per_interviewee[str(interviewee_id)] = questions

        # ✅ 질문 저장소에 등록
        QUESTION_STORE[interviewee_id] = questions
    
    return StartInterviewResponse(
        questions_per_interviewee=questions_per_interviewee,
        status="started"
    )

@router.post("/end", response_model=EndInterviewResponse)
async def end_interview(req: EndInterviewRequest):
    try:
        for iv in req.interviewees:
            state = INTERVIEW_STATE_STORE.get(iv.interviewee_id)
            if not state:
                raise HTTPException(status_code=404, detail=f"{iv.interviewee_id} 상태 없음")

            await process_last_audio_segment(state)
            save_nonverbal_counts(state, iv)

            await final_report_flow_executor(state)

        return EndInterviewResponse(result="done", report_ready=True)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stt/upload", response_model=STTUploadResponse)
async def upload_stt(
    interviewee_id: int = Form(...),
    audio: UploadFile = File(...),
):
    """
    답변 단위 음성 파일 업로드 및 STT 파이프라인 실행
    """
    try:
        # 1) 오디오 파일 저장
        file_path = await save_audio_file(interviewee_id, audio)
        if not file_path:
            raise HTTPException(status_code=500, detail="파일 저장 실패")

        # 2) 상태 가져오기 또는 새로 초기화
        state = INTERVIEW_STATE_STORE.get(interviewee_id)
        if state is None:
            questions = QUESTION_STORE.get(interviewee_id, [])  # 질문이 없으면 빈 리스트
            state = create_initial_state(interviewee_id, questions, file_path)
        else:
            state["audio_path"] = file_path

        # 3) 파이프라인 실행
        await interview_flow_executor(state)

        # 4) 상태 저장
        INTERVIEW_STATE_STORE[interviewee_id] = state

        return STTUploadResponse(result="OK")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
