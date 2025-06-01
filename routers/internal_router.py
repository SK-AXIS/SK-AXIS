from fastapi import APIRouter, HTTPException
from app.services.internal_client import fetch_interviewee_questions

router = APIRouter(prefix="/internal", tags=["Internal"])

@router.get("/interviewee/{interviewee_id}/questions")
async def get_interviewee_questions(interviewee_id: int):
    """
    Spring Boot에서 지원자별 면접 질문 5개를 조회
    """
    questions = await fetch_interviewee_questions(interviewee_id)
    if not questions:
        raise HTTPException(status_code=404, detail="해당 지원자 또는 질문 없음")
    return {"questions": questions} 