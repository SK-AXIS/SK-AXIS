from pydantic import BaseModel
<<<<<<< HEAD
from typing import Dict
class Posture(BaseModel):
    upright: int
    leaning: int
    slouching: int

class FacialExpression(BaseModel):
    smile: int
    neutral: int
    frown: int
    angry: int

class NonverbalData(BaseModel):
    interviewee_id: int
    posture: Posture
    facial_expression: FacialExpression
    gaze: int
    gesture: int

class NonverbalScore(BaseModel):
    interviewee_id: int
    posture_score: float
    facial_score: float
    overall_score: float
    feedback: Dict[str, str]
    detailed_analysis: str
    posture_raw_llm_response: str
    facial_raw_llm_response: str
    overall_raw_llm_response: str
=======
from typing import List, Optional

class NonverbalCounts(BaseModel):
    posture: int
    gaze: int
    expression: int
    gesture: int

class IntervieweeCounts(BaseModel):
    interviewee_id: int
    counts: NonverbalCounts

class EndInterviewRequest(BaseModel):
    interview_id: int
    interviewees: List[IntervieweeCounts]

class EndInterviewResponse(BaseModel):
    result: str
    report_ready: bool
>>>>>>> origin/main
