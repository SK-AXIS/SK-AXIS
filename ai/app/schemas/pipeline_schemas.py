# app/schemas/pipeline_schemas.py

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# ──────────────── 🔄 Rewrite 관련 스키마 ────────────────
class RewriteJudgeResult(BaseModel):
    """리라이팅 검증 결과 스키마"""
    ok: bool = Field(description="검증 통과 여부")
    judge_notes: List[str] = Field(description="검증 사유 목록")

class RewriteResult(BaseModel):
    """리라이팅 결과 스키마"""
    raw: str = Field(description="원본 텍스트")
    rewritten: str = Field(description="정제된 텍스트")
    timestamp: str = Field(description="처리 시간")

# ──────────────── 🧠 Evaluation 관련 스키마 ────────────────
class EvaluationCriterion(BaseModel):
    """개별 평가 기준 결과"""
    score: int = Field(ge=1, le=5, description="평가 점수 (1-5)")
    reason: str = Field(description="평가 사유")
    quotes: List[str] = Field(default_factory=list, description="인용구 목록")

class KeywordEvaluation(BaseModel):
    """키워드별 평가 결과"""
    SUPEX: EvaluationCriterion
    VWBE: EvaluationCriterion
    Passionate: EvaluationCriterion
    Proactive: EvaluationCriterion
    Professional: EvaluationCriterion
    People: EvaluationCriterion

class TechnicalEvaluation(BaseModel):
    """기술/직무 평가 결과"""
    실무_기술_지식: EvaluationCriterion
    문제_해결_적용력: EvaluationCriterion
    학습_발전_가능성: EvaluationCriterion

class DomainEvaluation(BaseModel):
    """도메인 전문성 평가 결과"""
    도메인_이해도: EvaluationCriterion
    실제_사례_적용: EvaluationCriterion
    전략적_사고력: EvaluationCriterion

class ContentValidationResult(BaseModel):
    """내용 검증 결과 스키마"""
    ok: bool = Field(description="검증 통과 여부")
    judge_notes: List[str] = Field(description="검증 사유 목록")

# ──────────────── 📊 Summary 관련 스키마 ────────────────
class ScoreSummary(BaseModel):
    """최종 점수 요약 스키마"""
    weights: Dict[str, float] = Field(description="영역별 가중치")
    personality_score: float = Field(description="인성적 요소 점수")
    job_domain_score: float = Field(description="직무/도메인 점수")
    verbal_score: float = Field(description="언어적 요소 총점")
    nonverbal_score: float = Field(description="비언어적 요소 점수")
    total_score: float = Field(description="최종 총점")
    verbal_reason: List[str] = Field(description="언어적 평가 요약")
    nonverbal_reason: str = Field(description="비언어적 평가 사유")
    keyword_scores: Dict[str, int] = Field(description="키워드별 총점")

# ──────────────── 😊 Nonverbal 관련 스키마 ────────────────
class NonverbalEvaluationResult(BaseModel):
    """비언어적 평가 결과 스키마"""
    score: float = Field(ge=0.0, le=1.0, description="평가 점수 (0.0-1.0)")
    analysis: str = Field(description="분석 내용")
    feedback: str = Field(description="피드백 내용") 