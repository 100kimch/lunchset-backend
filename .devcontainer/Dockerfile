# 멀티 플랫폼 지원 (ARM64 & x86_64)
ARG PLATFORM=linux/amd64
FROM --platform=$PLATFORM python:3.10

# 베이스 이미지 설정 (Python 3.10 사용)
FROM python:3.10

# 필수 패키지 업데이트 및 zsh 설치
RUN apt-get update && apt-get install -y zsh

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# FastAPI 소스 코드 복사
COPY app /app

# 기본 쉘을 zsh로 설정하며 FastAPI 실행
CMD ["zsh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
