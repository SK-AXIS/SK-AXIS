from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("/{applicant_id}")
async def get_questions(applicant_id: str = Path(..., description="지원자 ID")):
    return JSONResponse(content={
        "questions": [
            "자신의 장점을 말해주세요.",
            "팀 프로젝트에서의 갈등 해결 경험은?",
            "어떤 개발 도구를 주로 사용하는가?",
            "가장 성취감 있었던 프로젝트는?",
            "기술 역량 외의 강점은?"
        ]
    })