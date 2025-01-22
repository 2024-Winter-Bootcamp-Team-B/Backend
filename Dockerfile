# Dockerfile
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 libmariadb-dev gcc pkg-config libsm6 libxext6 libxrender-dev \ 
    && apt-get clean 

# 프로젝트 파일 복사
COPY . /app

# Celery Worker 실행 스크립트 실행 권한 부여
RUN chmod +x start_celery_flower.sh

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
