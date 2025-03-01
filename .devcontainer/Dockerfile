# 멀티 플랫폼 지원 (ARM64 & x86_64)
ARG PLATFORM=linux/arm64
FROM --platform=${PLATFORM} python:3.10

# 필수 패키지, oh-my-zsh 설치
RUN apt-get update && apt-get install -y sudo zsh curl git && \
  useradd -ms /bin/sh vscode && \
  echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode && \
  chmod 0440 /etc/sudoers.d/vscode

# Set default shell to zsh
SHELL ["/bin/zsh", "-c"]

WORKDIR /workspace
COPY /app ./app

# FastAPI 실행에 필요한 패키지 설치
COPY requirements.txt ./requirements.txt

# DevContainer에서는 테스트 패키지도 설치
COPY requirements.dev.txt ./requirements.dev.txt
RUN python -m pip install --upgrade pip && \
  cat ./requirements.txt && pip install --no-cache-dir -r ./requirements.txt && \
  cat ./requirements.dev.txt && pip install --no-cache-dir -r ./requirements.dev.txt

# 권한 설정 (vscode 사용자가 실행 가능하도록)
RUN chown -R vscode:vscode /workspace/app && \
  chsh -s $(which zsh) vscode

# vscode 사용자로 실행
USER vscode

# PATH 설정 추가, Zsh을 기본 셸로 변경
RUN echo 'export PATH=$HOME/.local/bin:$PATH' >> /home/vscode/.zshrc && \
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" || true

ENTRYPOINT ["/bin/zsh", "-c"]
CMD ["uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
