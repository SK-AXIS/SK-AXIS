from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# 라우터 import
from app.routers import (
    stt_router,
    interview_router
)

app = FastAPI(
    title="AI Interview System API",
    version="1.0",
    description="AI 기반 면접 평가 플랫폼의 API 문서"
)

# 정적 파일 서빙
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# 라우터 등록
app.include_router(stt_router.router, prefix="/stt", tags=["STT"])
app.include_router(interview_router.router, prefix="/interview", tags=["Interview"])

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 환경에서는 특정 도메인으로 제한해야 함
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
