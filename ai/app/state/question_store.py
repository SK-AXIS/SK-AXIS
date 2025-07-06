"""
SK AXIS AI 면접 시스템 - 질문 저장소

이 파일은 면접 질문 데이터를 메모리에 저장하는 전역 스토어입니다.
주요 기능:
- 면접자별 질문 목록 저장
- AI 평가 시 질문 참조용 데이터 제공

현재 상태:
- 구조는 정의되어 있지만 실제로는 작동하지 않음
- /interview/start 엔드포인트가 비활성화되어 있어 데이터가 채워지지 않음
- SpringBoot에서 질문 관리를 담당하고 있음

추후 활용 가능성:
- AI 기반 맞춤형 질문 생성 시 활용
- 실시간 질문 추천 로직 구현
- 질문-답변 매칭 분석
- 개인화된 질문 히스토리 관리

데이터 구조:
- Key: 면접자 ID (int)
- Value: 질문 객체 리스트 (List[Question])
"""

from typing import Dict, List, Any
from app.schemas.interview import Question

# ──────────────── 📝 질문 메모리 저장소 ────────────────

# 면접자별 질문 데이터를 저장하는 전역 딕셔너리
# 현재는 사용되지 않지만, 추후 AI 로직 확장 시 활용 가능
QUESTION_STORE: Dict[int, List[Question]] = {}

# 사용 예시 (추후 구현 시):
# QUESTION_STORE[123] = [
#     Question(question_id=1, type="공통질문", content="자기소개를 해주세요"),
#     Question(question_id=2, type="개별질문", content="프로젝트 경험을 설명해주세요")
# ]
#
# 현재 기준 활용 방안:
# 1. 질문-답변 분석: 질문 유형별 답변 품질 및 평가 개선