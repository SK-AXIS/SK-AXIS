from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 라우터 import
from app.routers import (
    stt_router,
    interview_router,
    internal_router
)

app = FastAPI(
    title="AI Interview System API",
    version="1.0",
    description="AI 기반 면접 평가 플랫폼의 API 문서"
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록
app.include_router(stt_router.router, prefix="/stt", tags=["STT"])
app.include_router(interview_router.router, prefix="/interview", tags=["Interview"])
app.include_router(internal_router.router)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 환경에서는 특정 도메인으로 제한해야 함
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
