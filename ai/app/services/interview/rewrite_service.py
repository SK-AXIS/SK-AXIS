"""
SK AXIS AI 면접 답변 리라이팅 서비스

이 파일은 STT(음성인식) 결과를 의미를 보존하면서 정제하는 서비스입니다.
주요 기능:
- STT 오류 및 문법 오류 수정
- 불필요한 공백 및 반복 제거
- 면접관 발언 필터링 (지원자 답변만 보존)
- 질문-답변 흐름 유지

처리 원칙:
- 지원자 답변의 핵심 의미는 절대 변경하지 않음
- 문법적 정확성 향상
- 면접 평가에 적합한 형태로 정제
- GPT-4o-mini 사용으로 비용 절약

사용 시점:
STT 완료 → rewrite_service → evaluation_service 순서로 파이프라인 진행
"""

import time
import os
from dotenv import load_dotenv
import openai

# ──────────────── 🔐 환경 설정 ────────────────
# Load environment variables and initialize API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ──────────────── 🧠 리라이팅 프롬프트 ────────────────
# 프롬프트: 의미 보존 + 문법/공백 정제 + 질문-답변 흐름 유지
REWRITE_PROMPT = """
다음은 면접 대화 STT 결과입니다. 지원자 답변의 의미는 변경하지 마세요.

처리 규칙:
- 문법 오류 및 오탈자 수정
- 불필요한 공백 제거
- 핵심 내용(질문-답변 흐름)은 그대로 보존
- 면접관 답변이 포착되면 해당 부분은 제거
- 지원자의 의도와 의미를 최대한 보존

원본 STT 결과:
{answer_raw}
"""

async def rewrite_answer(raw: str) -> tuple[str, float]:
    """
    STT로 받은 raw 텍스트를 의미 보존 기반으로 정제합니다.
    
    Args:
        raw (str): STT 원본 텍스트 (문법 오류, 공백 문제 등 포함)
        
    Returns:
        tuple[str, float]: (정제된 답변, 처리 시간 초)
        - 정제된 답변: 문법 수정 및 정리된 텍스트
        - 처리 시간: GPT API 호출 소요 시간 (초 단위)
        
    Note:
        - GPT-4o-mini 모델 사용 (비용 절약)
        - temperature=0.0으로 일관성 있는 결과 보장
        - 최대 1024 토큰으로 제한하여 비용 관리
    """
    # GPT 프롬프트에 원본 텍스트 삽입
    prompt = REWRITE_PROMPT.format(answer_raw=raw)
    
    # 처리 시간 측정 시작
    start = time.perf_counter()
    
    # OpenAI GPT API 호출
    response = openai.chat.completions.create(
        model="gpt-4o-mini",    # 비용 절약을 위해 mini 모델 사용
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,        # 출력 길이 제한 (비용 관리)
        temperature=0.0         # 일관성 있는 정제 결과를 위해 0으로 설정
    )
    
    # 처리 시간 계산
    elapsed = time.perf_counter() - start
    
    # GPT 응답에서 정제된 텍스트 추출
    rewritten = response.choices[0].message.content.strip()
    
    return rewritten, round(elapsed, 2)
