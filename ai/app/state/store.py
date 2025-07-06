"""
SK AXIS AI 면접 상태 전역 메모리 저장소

이 파일은 면접 진행 상태를 메모리에 저장하는 전역 저장소입니다.
주요 기능:
- 면접자별 상태 정보 임시 저장
- 파이프라인 단계별 처리 결과 보관
- API 간 상태 공유 및 조회 지원

저장소 구조:
- 키: interviewee_id (정수) - 면접자 고유 식별자
- 값: InterviewState (딕셔너리) - 해당 면접의 전체 상태

사용 패턴:
1. 면접 시작 시 초기 상태 생성 및 저장
2. 각 파이프라인 단계에서 상태 업데이트
3. API에서 상태 조회 및 결과 반환
4. 면접 완료 후 상태 정리 (선택적)

주의사항:
- 메모리 기반 저장소로 서버 재시작 시 데이터 소실
- 운영 환경에서는 Redis 등 영구 저장소 고려 필요
- 동시성 제어는 Python GIL에 의존
"""

from typing import Dict
from app.schemas.state import InterviewState

# ──────────────── 📦 전역 메모리 저장소 ────────────────
# 인터뷰 상태를 메모리에 저장하는 전역 스토어
# 키: interviewee_id (정수), 값: 해당 인터뷰의 상태 객체
INTERVIEW_STATE_STORE: Dict[int, InterviewState] = {}

# ──────────────── 🔧 사용 예시 ────────────────
# 상태 저장: INTERVIEW_STATE_STORE[101] = initial_state
# 상태 조회: state = INTERVIEW_STATE_STORE.get(101)
# 상태 업데이트: INTERVIEW_STATE_STORE[101]["stt"]["done"] = True
# 상태 삭제: del INTERVIEW_STATE_STORE[101]  # 선택적

