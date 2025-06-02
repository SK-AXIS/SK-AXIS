from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.routers import (
    interview_router,
    internal_router,
    stt_router,
    rewrite_router,
    nonverbal_router
)

# 환경 변수 로드
load_dotenv()

app = FastAPI(
    title="AI Interview System API",
    version="1.0",
    description="AI 기반 면접 평가 플랫폼의 API 문서"
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록
app.include_router(interview_router.router, prefix="/interview", tags=["Interview"])
app.include_router(internal_router.router)
app.include_router(rewrite_router.router, prefix="/api")
app.include_router(nonverbal_router.router, prefix="/api")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 특정 도메인만 허용하도록 수정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Interview Analysis API"}
