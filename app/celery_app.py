import requests
import os
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
    
############################################################################################################

UPLOAD_DIR = "uploaded_images"

@celery_app.task
def cleanup_user_files_task(user_id: int):
    """
    특정 사용자의 파일을 작업 완료된 순서대로 삭제하는 Celery 작업.
    """
    try:
        # 업로드된 파일 목록 가져오기
        user_files = [
            f for f in os.listdir(UPLOAD_DIR)
            if f.startswith(f"user_{user_id}_")  # 해당 사용자 ID에 해당하는 파일만 필터링
        ]

        # 타임스탬프 기준 정렬
        user_files.sort(key=lambda f: f.split("_")[2])  # 타임스탬프 추출 및 정렬

        # 가장 오래된 파일 삭제 -> 사용자가 여러번 업로드를 할 수도 있기 때문에
        if user_files:
            oldest_file = os.path.join(UPLOAD_DIR, user_files[0])
            os.remove(oldest_file)
            print(f"Deleted file: {oldest_file}")
        else:
            print(f"No files found for user {user_id} to delete.")

    except Exception as e:
        print(f"Error during cleanup for user {user_id}: {e}")