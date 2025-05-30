# app/services/interview/evaluation_service.py
import time
import os
from dotenv import load_dotenv
import openai

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# 키워드 추가 예정
# 5P 기반 Evaluation criteria definitions
EVAL_CRITERIA = {
    "Passionate": ["끈질긴 도전", "자신감과 열정", "고객 중심 문제 해결 노력"],
    "Professional": ["기술/역량 향상 노력", "동료 성장 기여", "리더십 역할 수행"],
    "Proactive": ["선제적 실행", "주도적 문제 해결", "개선 아이디어 제시"],
    "People": ["이타심", "팀워크 응원과 축하", "진정성 있는 소통"],
    "Personal": ["직무 전문성", "창의적 접근", "성과 중심 실행"]
}

EVAL_SYSTEM = "당신은 면접 평가 전문가입니다."
USER_TEMPLATE = """
지원자의 다음 답변에 대해, 역량({competency})를 기준으로
다음 세 가지 항목을 5점 만점으로 각각 평가하세요:
{criteria_list}

그리고 마지막에 이 3개 평가를 종합하여 100점 만점으로 환산된 '종합 점수'를 제시해주세요.

질문: {question}
답변: {answer}
"""

async def evaluate_answer(
    competency: str,
    question: str,
    answer: str
) -> tuple[dict[str, int], int, float]:
    """
    Evaluate a rewritten answer for a given 5P competency.
    Returns: (criteria_scores, total_score, elapsed_seconds)
    """
    criteria = EVAL_CRITERIA[competency]
    crit_text = "\n".join(f"- {c}" for c in criteria)
    prompt = USER_TEMPLATE.format(
        competency=competency,
        criteria_list=crit_text,
        question=question,
        answer=answer
    )
    start = time.perf_counter()
    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EVAL_SYSTEM},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=400
    )
    elapsed = time.perf_counter() - start
    content = resp.choices[0].message.content

    # Simple parsing of scores
    scores = {}
    for c in criteria:
        try:
            scores[c] = int(content.split(f"{c}:")[1].split("점")[0].strip())
        except:
            scores[c] = 0
    try:
        total = int(content.split("종합 점수:")[1].split("점")[0].strip())
    except:
        total = 0

    return scores, total, round(elapsed, 2)

# 벡터 기반 키워드 검색 보조
# from app.services.vector_service import search_related_keywords

# def enrich_evaluation_with_keywords(answer_text: str) -> str:
#     related = search_related_keywords(answer_text)
#     keyword_summary = "\n".join(f"- {r['term']}: {r['description']}" for r in related)
#     return keyword_summary
