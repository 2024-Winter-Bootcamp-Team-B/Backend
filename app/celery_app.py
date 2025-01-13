import requests
from celery import Celery
from app.services.mediapipe_service import analyze_image

# Celery 앱 객체 생성
celery_app = Celery(
    "app",  # 앱 이름
    broker="amqp://guest:guest@rabbitmq//",  # RabbitMQ URL
    # backend="db+mysql://celery_user:celery_password@mysql/celery_db"  # MySQL URL
)

# Celery 기본 설정
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=True,
)

# # 샘플 작업 추가 (테스트용)
# @celery_app.task
# def add(x, y):
#     return x + y

@celery_app.task
def process_image_task(image_path: str, requested_hand_shape: list):
    """
    Mediapipe를 사용해 이미지를 분석하고 결과를 FastAPI 서버로 전달.
    """
    try:
        # Mediapipe를 이용한 이미지 분석
        analysis_result = analyze_image(image_path, requested_hand_shape)

        # 결과를 FastAPI 서버로 전달
        response = requests.post(
            "http://fastapi:8000/api/save_analysis_result",
            json={
                "image_path": image_path,
                "result": analysis_result
            }
        )
        response.raise_for_status()  # 요청 에러 발생 시 예외 처리
        return analysis_result  # 작업 결과 반환
    except Exception as e:
        # 에러 로깅
        print(f"Error processing image: {e}")
        return {"error": str(e)}