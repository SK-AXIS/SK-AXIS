# app/routers/internal_router.py

from fastapi import APIRouter, HTTPException
from typing import List, Dict

<<<<<<< HEAD
from app.services.internal_client import fetch_interviewee_questions, fetch_multiple_interviewee_questions
=======
from app.services.internal_client import fetch_interviewee_questions
>>>>>>> origin/main
from app.schemas.interview import Question, MultipleIntervieweesRequest, MultipleIntervieweesResponse

router = APIRouter(tags=["Internal"])


@router.post(
    "/internal/interviewees/questions",
    response_model=MultipleIntervieweesResponse,
    summary="다중 지원자 질문 5개 조회 (FastAPI → Spring Boot)",
)
async def get_multiple_interviewee_questions(req: MultipleIntervieweesRequest):
    """
    Spring Boot ↔ FastAPI Internal API:
    - Body로 받은 여러 interviewee_id 리스트를 Spring Boot로 전달하여,
      각 지원자별 질문 5개를 한 번에 받아옵니다.
<<<<<<< HEAD
    - Spring Boot의 다중 지원자 질문 조회 API를 호출하여 한 번에 모든 지원자의 질문을 가져옵니다.
    """
    try:
        # 다중 지원자 질문 조회 API 호출
        questions_per_interviewee = await fetch_multiple_interviewee_questions(req.interviewee_ids)
        
        if not questions_per_interviewee:
            raise HTTPException(
                status_code=404,
                detail="지원자들의 질문을 찾을 수 없습니다."
            )
            
        return MultipleIntervieweesResponse(questions_per_interviewee=questions_per_interviewee)
    except Exception as e:
        # 오류 발생 시 대체 로직: 개별 API 호출로 폴백
        questions_per_interviewee: Dict[str, List[Question]] = {}
        
        for interviewee_id in req.interviewee_ids:
            try:
                raw_questions = await fetch_interviewee_questions(interviewee_id)
                if raw_questions:
                    questions_per_interviewee[str(interviewee_id)] = raw_questions
            except Exception:
                continue
        
        if not questions_per_interviewee:
            raise HTTPException(
                status_code=404,
                detail="모든 지원자의 질문을 찾을 수 없습니다."
            )
            
        return MultipleIntervieweesResponse(questions_per_interviewee=questions_per_interviewee)
=======
    - 현재 예시에서는 Spring Boot에 '한 번에 다중 조회' API가 없다고 가정하고,
      내부적으로 fetch_interviewee_questions()를 ID마다 반복 호출합니다.
    """
    questions_per_interviewee: Dict[str, List[Question]] = {}

    for interviewee_id in req.interviewee_ids:
        raw_questions = await fetch_interviewee_questions(interviewee_id)
        if not raw_questions:
            # 하나라도 실패하면 404 반환
            raise HTTPException(
                status_code=404,
                detail=f"지원자 {interviewee_id}의 질문을 찾을 수 없습니다."
            )
        # raw_questions는 List[Dict] 형태로 받아오므로, Pydantic Question 모델로 가정
        questions_per_interviewee[str(interviewee_id)] = raw_questions

    return MultipleIntervieweesResponse(questions_per_interviewee=questions_per_interviewee)
>>>>>>> origin/main
