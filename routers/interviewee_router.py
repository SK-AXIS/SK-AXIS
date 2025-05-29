from fastapi import APIRouter, Query
from typing import Optional, List

router = APIRouter(prefix="/interviewees", tags=["Interviewees"])

@router.get("")
async def list_interviewees(
    date: Optional[str] = Query(None),
    status: Optional[str] = Query(None, enum=["대기중", "진행중", "완료", "취소"]),
    position: Optional[str] = Query(None)
):
    # TODO: Query database with filters
    return {
        "data": [],
        "total_count": 0
    }
