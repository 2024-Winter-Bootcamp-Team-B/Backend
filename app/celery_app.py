import requests
import os
from celery import Celery
from app.services.mediapipe_service import analyze_image
from datetime import datetime
import re

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
    print("----celery----")
    """
     Mediapipe를 사용해 이미지를 분석하고 결과를 FastAPI 서버로 전달.
    """
    try:
        # 파일 경로 유효성 확인 코드 추가
        print(f"Looking for file at: {image_path}")  # 디버깅용 로그 추가

        if not os.path.exists(image_path):
            print(f"File not found: {image_path}")
            raise ValueError(f"File not found: {image_path}")
        
        pattern = r"user_(\d+)_(\d{8}T\d{6}Z)_"
        match = re.search(pattern, image_path)
        if match:
            user_id = int(match.group(1))  # 첫 번째 그룹: user_id
            timestamp = match.group(2)  # 두 번째 그룹: timestamp
            response_info = {"user_id": user_id, "timestamp": timestamp}
        else:
            raise ValueError(f"Invalid image_path format: {image_path}")

        # Mediapipe를 이용한 이미지 분석
        analysis_result = analyze_image(image_path, requested_hand_shape)

        # 결과를 FastAPI 서버로 전달 -> 아래와 같은 구조로 전달됨

        # {
        #     "user_id": "user_id값",  // 이미지와 연결된 사용자 ID
        #     "timestamp": "ISO형식 타임스탬프",  // 요청의 생성 시간
        #     "result": {  // analyze_image의 결과값 포함
        #         "match": true,
        #         "message": "손 모양이 요청한 모양과 일치합니다."
        #     }
        # }

        # ISO 8601 형식의 타임스탬프를 datetime 객체로 변환 (검증)
        timestamp_iso = datetime.strptime(response_info["timestamp"], "%Y%m%dT%H%M%SZ").isoformat()

        # 결과를 FastAPI 서버로 전달
        try:
            response = requests.post(
                "http://fastapi:8000/photo/result",
                json={
                    "user_id": response_info["user_id"],
                    "timestamp": timestamp_iso,  # ISO 형식 타임스탬프
                    "result": 1 if analysis_result["match"] else 0,  # match 값을 정수로 변환
                }
            )

            # if response.status_code == 400:
            #     print(f"[INFO] 차단 해제 요청 거부: {response.json().get('error')}")
            # elif response.status_code == 200:
            #     print("[INFO] 차단 해제가 성공적으로 처리되었습니다.")
            # else:
            #     print(f"[INFO] 예상치 못한 응답 상태 코드: {response.status_code}")

            response.raise_for_status()  # 요청 에러 발생 시 예외 처리

            # 요청 성공 시 로그 추가
            print(f"POST request to /photo/result successful: {response.status_code}")
            print(f"Response content: {response.json()}")

        except requests.RequestException as e:
            # 요청 실패 시 로그 추가
            print(f"Error sending POST request to /photo/result: {e}")
            raise

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