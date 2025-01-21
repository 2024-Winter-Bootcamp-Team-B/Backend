from fastapi import APIRouter, File, UploadFile, HTTPException # File, UploadFile: 파일 업로드를 처리하기 위한 FastAPI 유틸리티.
from fastapi.responses import JSONResponse # JSONResponse: JSON 형식으로 응답을 반환
from datetime import datetime
from uuid import uuid4
import os # os, shutil: 파일 저장 및 관리에 사용
import shutil
from app.services.mediapipe_service import analyze_image # analyze_image: Mediapipe 로직이 구현된 서비스 모듈을 가져옴
from app.celery_app import process_image_task  # Celery 작업 불러오기
from fastapi import Form


router = APIRouter()

UPLOAD_DIR = "uploaded_images"

@router.post("/lock/upload-image")
async def upload_image(user_id: int = Form(...) , file: UploadFile = File(...)):
    """
    고유 파일명을 생성하여 저장하고, 파일 경로를 반환. 파일 삭제는 별도 처리에서 호출.
    """
    try:
        print(f"User ID: {user_id}, File Name: {file.filename}")
        print("TEST O1")
        # 디렉토리 생성
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # 고유 파일명 생성
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        unique_filename = f"user_{user_id}_{timestamp}_{uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # 파일 MIME 타입 확인
        if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            raise HTTPException(status_code=400, detail="Only JPEG or PNG or JPG files are allowed")

        # 파일 저장
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Error saving the file: {str(e)}")
        

        # Celery 작업 호출 -> 아무리 봐도 셀러리 작업을 여기서 호출하는게 맞는거 같음

        requested_hand_shape = [1, 1, 1, 1, 1]  # 예: 다섯 손가락 모두 펴짐 
        print("TEST 02")
        ###### 이거는 나중에 수정해야함 -> 프론트에서 넘어온 값으로
        task = process_image_task.delay(file_path, requested_hand_shape)
        print("TEST 03")
        return {
            "message": "File uploaded and analysis started",
            "file_path": file_path,
            "task_id": task.id  # 작업 ID 반환
        }

        # return file_path

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while processing the file: {str(e)}")
