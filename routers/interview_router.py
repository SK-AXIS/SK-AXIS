from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv

from app.schemas.interview import StartInterviewRequest, StartInterviewResponse, EndInterviewResponse, \
    EndInterviewRequest
from app.services.pipeline_service import run_pipeline
from app.services.internal_client import fetch_interviewee_questions

# 환경 변수 로드
load_dotenv()

router = APIRouter(prefix="/interview", tags=["Interview"])

# 결과 저장 경로 설정
RESULT_DIR = os.getenv("RESULT_DIR", "./result")
os.makedirs(RESULT_DIR, exist_ok=True)

@router.post("/start", response_model=StartInterviewResponse)
async def start_interview(req: StartInterviewRequest):
    # Spring Boot에서 질문 5개 받아오기
    questions = await fetch_interviewee_questions(req.interviewee_id)
    if not questions:
        raise HTTPException(status_code=404, detail="질문을 찾을 수 없습니다.")
    return StartInterviewResponse(questions=questions, status="started")

@router.post("/end", response_model=EndInterviewResponse)
async def end_interview(req: EndInterviewRequest):
    try:
        # 인터뷰 ID에 따른 STT 결과 JSON 경로 설정
        json_input_path = f"./data/interview_{req.interview_id}_stt.json"
        radar_chart_path = os.path.join(RESULT_DIR, f"interview_{req.interview_id}_chart.png")
        pdf_output_path = os.path.join(RESULT_DIR, f"interview_{req.interview_id}_report.pdf")

        if not os.path.exists(json_input_path):
            raise FileNotFoundError(f"STT JSON 파일이 존재하지 않습니다: {json_input_path}")

        # 비동기 파이프라인 실행
        await run_pipeline(
            input_json=json_input_path,
            chart_path=radar_chart_path,
            output_pdf=pdf_output_path
        )

        return EndInterviewResponse(result="done", report_ready=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))