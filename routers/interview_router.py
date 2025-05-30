from fastapi import APIRouter, HTTPException
import os

from app.schemas.interview import StartInterviewRequest, StartInterviewResponse, EndInterviewResponse, \
    EndInterviewRequest
from app.services.pipeline_service import run_pipeline

router = APIRouter(prefix="/interview", tags=["Interview"])

@router.post("/start", response_model=StartInterviewResponse)
async def start_interview(req: StartInterviewRequest):
    # 예시용 질문 5개를 반환하는 더미 데이터
    dummy_questions = [
        {"question_id": 3001, "type": "공통질문", "content": "자신의 장점을 말씀해 주세요."},
        {"question_id": 3002, "type": "공통질문", "content": "최근에 도전한 경험은 무엇인가요?"},
        {"question_id": 3003, "type": "공통질문", "content": "팀에서의 갈등을 해결한 경험을 말씀해 주세요."},
        {"question_id": 3004, "type": "공통질문", "content": "창의적으로 문제를 해결한 경험이 있다면?"},
        {"question_id": 3005, "type": "공통질문", "content": "목표를 끝까지 이루기 위해 노력한 경험은?"}
    ]
    return StartInterviewResponse(questions=dummy_questions, status="started")

@router.post("/end", response_model=EndInterviewResponse)
async def end_interview(req: EndInterviewRequest):
    try:
        # 인터뷰 ID에 따른 STT 결과 JSON 경로 설정 (예시)
        json_input_path = f"./data/interview_{req.interview_id}_stt.json"
        radar_chart_path = f"d:/result/interview_{req.interview_id}_chart.png"
        pdf_output_path = f"d:/result/interview_{req.interview_id}_report.pdf"

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