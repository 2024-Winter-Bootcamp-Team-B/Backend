from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.lock import unblock_sites_by_user
from app.services.mediapipe_service import analyze_image
from app.celery_app import cleanup_user_files_task  # Celery 작업 불러오기

import os
import shutil

router = APIRouter()

@router.post("/lock/unblock/{user_id}")
async def unblock_sites(user_id: int, result: int, db: Session = Depends(get_db)):
    """
    차단 해제 API: 손 모양이 요청된 형태와 일치할 경우 차단된 사이트 해제
    """
    try:
        # 1. 분석 결과 확인
        if result != 1:  # 1이 아니면 요청 거절
            raise HTTPException(
                status_code=400,
                detail="손 모양이 요청한 모양과 일치하지 않아서 차단 해제를 진행하지 않았습니다."
            )
        print(f"Processing unblock request for user_id: {user_id} with result: {result}")

        # 2. 차단된 사이트 해제
        unblock_sites_by_user(db, user_id)
        print(f"Unblocked sites for user_id: {user_id}")

        # 3. Celery 작업으로 파일 정리
        cleanup_user_files_task.delay(user_id)
        print(f"Scheduled cleanup task for user_id: {user_id}")

        # 4. 성공 응답 반환
        return {"message": "모든 차단된 사이트가 해제되었습니다.", "user_id": user_id}


    except Exception as e:
        # 에러 발생 시 JSON 에러 메시지 반환 -> *** 이거 나중에 리다이렉션 페이지로 가도록 수정해야함
        return JSONResponse(content={"error": str(e)}, status_code=500)

    # finally:
    #     # 업로드된 파일 삭제
    #     if os.path.exists(file_path):
    #         os.remove(file_path)