# app/schemas/interview.py

from pydantic import BaseModel
from typing import List, Literal


class StartInterviewRequest(BaseModel):
    interviewee_id: int
    interviewer_id: int


class Question(BaseModel):
    question_id: int
    type: Literal["공통질문", "개별질문"]
    content: str


class StartInterviewResponse(BaseModel):
    questions: List[Question]
    status: str


class EndInterviewRequest(BaseModel):
    interview_id: int


class EndInterviewResponse(BaseModel):
    result: str
    report_ready: bool
