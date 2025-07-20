# app/services/pipeline/pipeline_builder.py

from langgraph.graph import StateGraph
from app.schemas.state import InterviewState
from .pipeline_nodes import stt_node, should_retry_rewrite, should_retry_evaluation
from .pipeline_agents import (
    rewrite_agent, rewrite_judge_agent, nonverbal_evaluation_agent,
    evaluation_agent, evaluation_judge_agent, score_summary_agent
)

def build_interview_flow() -> StateGraph:
    """
    STT → 리라이팅 파이프라인 구성
    
    Returns:
        StateGraph: 인터뷰 플로우 그래프
        
    파이프라인 구조:
    1. stt_node: 음성 → 텍스트 변환
    2. rewrite_agent: 텍스트 정제 및 문법 수정
    3. rewrite_judge_agent: 정제 결과 품질 검증
    4. 재시도 로직 (현재 비활성화)
    """
    interview_builder = StateGraph(InterviewState)
    
    # 노드 추가
    interview_builder.add_node("stt_node", stt_node)
    interview_builder.add_node("rewrite_agent", rewrite_agent)
    interview_builder.add_node("rewrite_judge_agent", rewrite_judge_agent)
    
    # 시작점 설정
    interview_builder.set_entry_point("stt_node")
    
    # 엣지 연결
    interview_builder.add_edge("stt_node", "rewrite_agent")
    interview_builder.add_edge("rewrite_agent", "rewrite_judge_agent")
    
    # 조건부 엣지 (재시도 로직)
    interview_builder.add_conditional_edges(
        "rewrite_judge_agent", should_retry_rewrite,
        {"retry": "rewrite_agent", "done": "__end__"}
    )
    
    return interview_builder

def build_final_flow() -> StateGraph:
    """
    평가 → 요약 파이프라인 구성
    
    Returns:
        StateGraph: 최종 평가 플로우 그래프
        
    파이프라인 구조:
    1. nonverbal_evaluation_agent: 표정 기반 비언어적 평가
    2. evaluation_agent: 8개 키워드 × 3개 기준 = 24개 항목 평가
    3. evaluation_judge_agent: 평가 결과 검증 및 내용 검증
    4. score_summary_agent: 100점 만점 환산 및 최종 요약
    5. 재시도 로직 (최대 1회)
    """
    final_builder = StateGraph(InterviewState)
    
    # 노드 추가
    final_builder.add_node("nonverbal_eval", nonverbal_evaluation_agent)
    final_builder.add_node("evaluation_agent", evaluation_agent)
    final_builder.add_node("evaluation_judge_agent", evaluation_judge_agent)
    final_builder.add_node("score_summary_agent", score_summary_agent)
    
    # 시작점 설정
    final_builder.set_entry_point("nonverbal_eval")
    
    # 엣지 연결
    final_builder.add_edge("nonverbal_eval", "evaluation_agent")
    final_builder.add_edge("evaluation_agent", "evaluation_judge_agent")
    
    # 조건부 엣지 (재시도 로직)
    final_builder.add_conditional_edges(
        "evaluation_judge_agent", should_retry_evaluation,
        {"retry": "evaluation_agent", "continue": "score_summary_agent", "done": "__end__"}
    )
    
    return final_builder

# 전역 인스턴스 생성
interview_flow_executor = build_interview_flow().compile()
final_flow_executor = build_final_flow().compile() 