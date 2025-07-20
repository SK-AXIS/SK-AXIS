# app/services/pipeline/pipeline_chains.py

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.schemas.pipeline_schemas import (
    RewriteJudgeResult,
    ContentValidationResult,
    NonverbalEvaluationResult
)

class PipelineChains:
    """파이프라인 체이닝 컴포넌트 관리 클래스"""
    
    def __init__(self):
        self.llm_mini = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.llm_full = ChatOpenAI(model="gpt-4o", temperature=0)
    
    @property
    def rewrite_judge_chain(self):
        """리라이팅 검증 체인"""
        parser = JsonOutputParser(pydantic_object=RewriteJudgeResult)
        prompt = PromptTemplate(
            template="""
시스템: 당신은 텍스트 리라이팅 평가 전문가입니다.
원본: "{raw}"
리라이팅: "{rewritten}"

1) 의미 보존
2) 과잉 축약/확장  
3) 오탈자/문맥 오류

위 기준에 따라 평가하세요.

{format_instructions}
            """,
            input_variables=["raw", "rewritten"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        return prompt | self.llm_mini | parser
    
    @property
    def content_validation_chain(self):
        """평가 내용 검증 체인"""
        parser = JsonOutputParser(pydantic_object=ContentValidationResult)
        prompt = PromptTemplate(
            template="""
시스템: 당신은 AI 면접 평가 결과의 검증 전문가입니다.

[지원자 답변]
{answer}

[평가 결과]
{evaluation}

[평가 기준]
{criteria}

평가 결과를 검증하고 아래 형식으로 답변하세요.

{format_instructions}
            """,
            input_variables=["answer", "evaluation", "criteria"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        return prompt | self.llm_mini | parser
    
    @property
    def nonverbal_evaluation_chain(self):
        """비언어적 평가 체인"""
        parser = JsonOutputParser(pydantic_object=NonverbalEvaluationResult)
        prompt = PromptTemplate(
            template="""
시스템: 당신은 면접 중 표정 분석 전문가입니다.

[표정 데이터]
{facial_data}

표정 패턴을 분석하여 평가하세요.

{format_instructions}
            """,
            input_variables=["facial_data"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        return prompt | self.llm_mini | parser
    
    @property
    def score_summary_chain(self):
        """점수 요약 체인"""
        prompt = PromptTemplate(
            template="""
아래는 지원자의 전체 답변과 각 평가 키워드별 평가 사유입니다.

[지원자 답변]
{answer}

[평가 사유]
{all_reasons}

이 두 정보를 참고하여, 지원자가 이렇게 점수를 얻게 된 이유를 8줄 이내로 자연스럽게 요약해 주세요.
- 평가 근거와 지원자의 핵심 답변 내용이 모두 포함되도록 하세요.
- 각 줄은 간결하고 핵심적으로 작성해 주세요.
- 중복되는 내용은 합치고, 중요한 특징/강점/보완점이 드러나도록 해 주세요.
- 반드시 8줄 이내로만 작성하세요.
            """,
            input_variables=["answer", "all_reasons"]
        )
        return prompt | self.llm_full

# 전역 인스턴스
chains = PipelineChains() 