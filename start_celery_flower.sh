#!/bin/sh

# set two worker for testing purposes. 큐 하나당 워커 하나면 됨

# 패키지 업데이트 및 설치
apt-get update
apt-get install -y libgl1 libglib2.0-0 libmariadb-dev gcc pkg-config

# Python 패키지 설치
pip install --no-cache-dir -r requirements.txt

celery -A app.celery_app worker --loglevel=info --concurrency=1 -n worker_1_@%h & # 워커 1번 %h는 호스트 이름으로 대체.
# celery -A app.celery_app worker --loglevel=info --concurrency=1 -n worker_2_@%h & # 워커 2번 %h는 호스트 이름으로 대체.

celery -A app.celery_app flower --port=5555 --basic_auth=guest:guest --broker=$CELERY_BROKER_URL --broker_api=$CELERY_BROKER_API_URL #플라워 시작