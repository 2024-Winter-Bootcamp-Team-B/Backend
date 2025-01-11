from fastapi import APIRouter, File, UploadFile # File, UploadFile: 파일 업로드를 처리하기 위한 FastAPI 유틸리티.
from fastapi.responses import JSONResponse # JSONResponse: JSON 형식으로 응답을 반환
import os # os, shutil: 파일 저장 및 관리에 사용
import shutil
from app.services.mediapipe_service import analyze_image # analyze_image: Mediapipe 로직이 구현된 서비스 모듈을 가져옴

router = APIRouter()

@router.post("/lock/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    이미지 업로드 후 Mediapipe로 분석. -> true, false, error 반환
    """
    try:
        # 업로드된 이미지 저장
        upload_dir = "uploaded_images"  # 이미지가 저장될 디렉토리
        os.makedirs(upload_dir, exist_ok=True)  # 디렉토리가 없으면 생성
        file_path = os.path.join(upload_dir, file.filename)  # 파일 경로 설정
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)  # 업로드된 파일 저장

        # Mediapipe 처리
        requested_hand_shape = [1, 1, 0, 1, 1]  # 요청된 손 모양
        result = analyze_image(file_path, requested_hand_shape)  # 분석 결과 반환

        return JSONResponse(content=result)  # 결과를 JSON으로 반환

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)  # 예외 발생 시 에러 메시지 반환

    finally:
        # 업로드된 파일 삭제
        if os.path.exists(file_path):
            os.remove(file_path)  # 서버에 남은 파일 삭제