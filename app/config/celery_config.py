# celery_config.py
# 별도의 파일에서 celery 작업을 정의하기 위한 구성.
import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv() # 환경 변수를 불러오기 위한 코드

celery_app = Celery(
	__name__, 
	broker=os.getenv("CELERY_BROKER_URL"), 
	backend=os.getenv("CELERY_RESULT_BACKEND")
)

celery_app.conf.update(
   # imports=['app.tasks.celery_tasks'], # celery 작업 파일 경로
    broker_connection_retry_on_startup=True,
    task_track_started=True
)