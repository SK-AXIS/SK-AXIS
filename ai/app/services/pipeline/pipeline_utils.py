# app/services/pipeline/pipeline_utils.py

from datetime import datetime
import pytz
from typing import Dict, Any, Optional
from app.schemas.state import InterviewState

KST = pytz.timezone('Asia/Seoul')

class PipelineUtils:
    """파이프라인 유틸리티 함수들"""
    
    @staticmethod
    def safe_get(d: Dict, key: str, default=None, context: str = "") -> Any:
        """안전한 딕셔너리 접근 함수"""
        try:
            return d.get(key, default)
        except Exception as e:
            print(f"[ERROR] [{context}] get('{key}') 예외 발생: {e}")
            return default
    
    @staticmethod
    def add_decision_log(state: InterviewState, step: str, result: str, details: Dict = None) -> None:
        """결정 로그 추가"""
        state.setdefault("decision_log", []).append({
            "step": step,
            "result": result,
            "time": datetime.now(KST).isoformat(),
            "details": details or {}
        })
    
    @staticmethod
    def calculate_area_scores(evaluation_results: Dict, nonverbal_score: int) -> tuple:
        """영역별 점수 계산 및 100점 만점 환산"""
        personality_keywords = ["SUPEX", "VWBE", "Passionate", "Proactive", "Professional", "People"]
        job_domain_keywords = ["기술/직무", "도메인 전문성"]
        
        # 언어적 요소 총점
        personality_score = 0
        for keyword in personality_keywords:
            for criterion in evaluation_results.get(keyword, {}).values():
                personality_score += criterion.get("score", 0)
        
        # 직무·도메인 총점
        job_domain_score = 0
        for keyword in job_domain_keywords:
            for criterion in evaluation_results.get(keyword, {}).values():
                job_domain_score += criterion.get("score", 0)
        
        # 100점 만점 환산
        max_personality = 90
        max_job_domain = 30
        max_nonverbal = 15
        
        personality_score_scaled = round((personality_score / max_personality) * 45, 1) if max_personality else 0
        job_domain_score_scaled = round((job_domain_score / max_job_domain) * 45, 1) if max_job_domain else 0
        nonverbal_score_scaled = round((nonverbal_score / max_nonverbal) * 10, 1) if max_nonverbal else 0
        
        weights = {
            "인성적 요소": 45.0,
            "직무·도메인": 45.0,
            "비언어적 요소": 10.0
        }
        
        return weights, personality_score_scaled, job_domain_score_scaled, nonverbal_score_scaled

# 전역 인스턴스
utils = PipelineUtils() 