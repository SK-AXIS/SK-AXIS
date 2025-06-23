# Multi-stage build 사용
FROM python:3.9-slim AS builder

# 빌드 의존성만 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 의존성 설치
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 실행 단계
FROM python:3.9-slim

<<<<<<< HEAD
WORKDIR /app

# 시스템 패키지 설치 (OpenCV & MediaPipe 작동 최소 패키지)
=======
# 런타임 의존성만 설치
>>>>>>> origin/main
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libpulse0 \
    libportaudio2 \
    ffmpeg \
    build-essential \
    portaudio19-dev \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

<<<<<<< HEAD
# Python 의존성 설치 (한 RUN으로 pip install 묶기)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
        opencv-python-headless==4.9.0.80 \
        mediapipe==0.10.5 \
        openai-whisper \
        google-cloud-speech \
        pyaudio \
        pydub \
        fastapi \
        uvicorn \
        python-multipart \
        websockets \
        aiofiles \
        httpx \
        reportlab \
        pandas \
        openpyxl \
        python-dotenv

# 코드 복사 및 디렉토리 생성
=======
# 빌더에서 Python 패키지 복사
COPY --from=builder /root/.local /root/.local

# PATH 설정
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app
>>>>>>> origin/main
COPY . .
RUN mkdir -p output app/uploads app/temp static

<<<<<<< HEAD
RUN mkdir -p \
    output \
    app/uploads \
    app/temp \
    static

# 환경 변수
ENV OPENAI_API_KEY=""
ENV SPRING_API_URL="http://springboot:8080/api/v1"
ENV OUTPUT_DIR="/app/output"
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=1

# 포트 노출
EXPOSE 8000

# 실행 커맨드
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
=======
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> origin/main
