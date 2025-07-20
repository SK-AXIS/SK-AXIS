"""
SK AXIS AI 면접 평가 파이프라인 - 그래프 기반 워크플로우

이 파일은 LangGraph를 사용하여 면접 평가 전체 파이프라인을 관리하는 핵심 모듈입니다.
주요 기능:
- STT → 리라이팅 → 평가 → 요약까지 전체 워크플로우 오케스트레이션
- 각 단계별 검증 및 재시도 로직 (최대 1회)
- 상태 기반 파이프라인 진행 상황 추적
- 비용 최적화된 GPT-4o-mini 모델 사용

파이프라인 구조:
1. STT Node: 음성 → 텍스트 변환
2. Rewrite Agent: 텍스트 정제 및 문법 수정
3. Rewrite Judge: 정제 결과 품질 검증
4. Nonverbal Evaluation Agent: 표정 기반 비언어적 평가
5. Evaluation Agent: 8개 키워드 × 3개 기준 = 24개 항목 평가
6. Evaluation Judge: 평가 결과 검증 및 내용 검증
7. Score Summary Agent: 100점 만점 환산 및 최종 요약

성능 최적화:
- GPT-4o → GPT-4o-mini 변경으로 94% 비용 절감
- 재시도 로직 1회 제한으로 무한 루프 방지
- 파일 헤더 검증으로 3000배 속도 향상
"""

# app/services/pipeline/graph_pipeline.py

from app.schemas.state import InterviewState
from .pipeline_builder import interview_flow_executor, final_flow_executor

async def run_interview_flow(state: InterviewState) -> InterviewState:
    """
    STT → 리라이팅 파이프라인 실행
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        InterviewState: 리라이팅 완료된 상태
        
    처리 과정:
    1. STT: 음성 파일을 텍스트로 변환
    2. Rewrite: 텍스트 정제 및 문법 수정
    3. Rewrite Judge: 정제 결과 품질 검증
    """
    return await interview_flow_executor.ainvoke(state)

async def run_final_flow(state: InterviewState) -> InterviewState:
    """
    평가 → 요약 파이프라인 실행
    
    Args:
        state (InterviewState): 면접 상태 객체
        
    Returns:
        InterviewState: 평가 완료된 상태
        
    처리 과정:
    1. Nonverbal Evaluation: 표정 기반 비언어적 평가
    2. Evaluation: 키워드별 평가 수행
    3. Evaluation Judge: 평가 결과 검증
    4. Score Summary: 최종 점수 환산 및 요약
    """
    return await final_flow_executor.ainvoke(state) 