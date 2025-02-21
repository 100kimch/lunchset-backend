# 멀티 플랫폼 지원 (ARM64 & x86_64)
ARG PLATFORM=linux/arm64
FROM --platform=${PLATFORM} python:3.10

# zsh 설치 후 기본 설정 추가
RUN apt-get update && apt-get install -y zsh sudo && \
  useradd -ms /bin/zsh vscode && \
  echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
  echo "# Zsh configuration" > /root/.zshrc && \
  echo "export SHELL=/usr/bin/zsh" >> /root/.zshrc && \
  echo "exec /usr/bin/zsh" >> /root/.zshrc

WORKDIR /app

# 패키지 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# FastAPI 소스 코드 복사
COPY app /app

# 기본 사용자 설정
USER vscode

# 기본 쉘을 zsh로 설정하며 FastAPI 실행
CMD ["zsh", "-c", "cd /app && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
