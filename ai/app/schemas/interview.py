from pydantic import BaseModel
from typing import List, Dict, Literal

class Posture(BaseModel):
    upright: int
    leaning: int
    slouching: int

class FacialExpression(BaseModel):
    smile: int
    neutral: int
    frown: int
    angry: int

class IntervieweeNonverbalData(BaseModel):
    posture: Posture
    facial_expression: FacialExpression
    gaze: int
    gesture: int
    timestamp: int

class StartInterviewRequest(BaseModel):
    interviewee_ids: List[int]
    interviewer_ids: List[int]

class Question(BaseModel):
    question_id: int
    type: Literal["공통질문", "개별질문"]
    content: str

class StartInterviewResponse(BaseModel):
    questions_per_interviewee: Dict[str, List[Question]]
    status: str

class EndInterviewRequest(BaseModel):
    interview_id: int
    data: Dict[str, IntervieweeNonverbalData]

class EndInterviewResponse(BaseModel):
    result: str
    report_ready: bool

class QuestionsResponse(BaseModel):
    questions: List[Question]

class MultipleIntervieweesRequest(BaseModel):
    interviewee_ids: List[int]

class MultipleIntervieweesResponse(BaseModel):
    questions_per_interviewee: Dict[str, List[Question]]

class STTUploadResponse(BaseModel):
    result: str
