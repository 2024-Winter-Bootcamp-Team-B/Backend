from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.lock import unblock_sites_by_user
from app.services.mediapipe_service import analyze_image

import os
import shutil

router = APIRouter()

@router.post("/lock/unblock/{user_id}")
async def unblock_sites(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    차단 해제 API: 손 모양이 요청된 형태와 일치할 경우 차단된 사이트 해제
    """
    # 요청된 손 모양 정의 (예: 다섯 손가락 모두 펴짐)
    requested_hand_shape = [1, 1, 1, 1, 1]

    # 이미지 저장 경로 설정
    upload_dir = "uploaded_images"  # 이미지 저장 디렉토리
    os.makedirs(upload_dir, exist_ok=True)  # 디렉토리가 없으면 생성
    file_path = os.path.join(upload_dir, file.filename)  # 저장할 파일 경로

    try:
        # 업로드된 파일 저장
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Mediapipe로 손 모양 분석
        result = analyze_image(file_path, requested_hand_shape)

        # 분석 결과 확인
        if not result["match"]:
            raise HTTPException(status_code=400, detail=result["message"])

        # 차단된 사이트 해제
        unblock_sites_by_user(db, user_id)

        return {"message": "모든 차단된 사이트가 해제되었습니다.", "user_id": user_id}

    except Exception as e:
        # 에러 발생 시 JSON 에러 메시지 반환 -> *** 이거 나중에 리다이렉션 페이지로 가도록 수정해야함
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        # 업로드된 파일 삭제
        if os.path.exists(file_path):
            os.remove(file_path)