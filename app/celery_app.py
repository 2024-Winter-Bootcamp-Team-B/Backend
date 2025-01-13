from celery import Celery

# Celery 앱 객체 생성
celery_app = Celery(
    "app",  # 앱 이름
    broker="amqp://guest:guest@rabbitmq//",  # RabbitMQ URL
    backend="redis://redis:6379/0"          # Redis URL
)

# Celery 기본 설정
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=True,
)

# 샘플 작업 추가 (테스트용)
@celery_app.task
def add(x, y):
    return x + y