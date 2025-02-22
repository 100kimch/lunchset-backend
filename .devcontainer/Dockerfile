# 멀티 플랫폼 지원 (ARM64 & x86_64)
ARG PLATFORM=linux/arm64
FROM --platform=${PLATFORM} python:3.10

# 필수 패키지 설치
RUN apt-get update && apt-get install -y sudo && \
  useradd -ms /bin/sh vscode && \
  echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /app
COPY ./app .

# FastAPI 실행에 필요한 패키지 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 권한 설정 (vscode 사용자가 실행 가능하도록)
RUN chown -R vscode:vscode /app

# vscode 사용자로 실행
USER vscode

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
