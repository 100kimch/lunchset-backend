# Lunchset-backend

- Prototype project using FastAPI

## Docker 빌드

```bash
docker build -t lunchset-backend .
```

## Docker 실행

```bash
docker run -p 8000:8000 lunchset-backend
```

## container 제거

```bash
docker rm -f $(docker ps -aq)  # 기존 컨테이너 삭제
docker volume prune -f          # 사용하지 않는 볼륨 삭제
docker system prune -af         # 불필요한 캐시 제거
```

## docker compose 리빌드

```bash
docker compose -f .devcontainer/docker-compose.dev.yml up --build
```
