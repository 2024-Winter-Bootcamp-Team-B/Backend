from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from fastapi.responses import JSONResponse
from httpx import request
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.lock import unblock_sites_by_user
from app.services.mediapipe_service import analyze_image
from app.celery_app import cleanup_user_files_task  # Celery 작업 불러오기
from pydantic import BaseModel

import os
import shutil

router = APIRouter()

# 내부 호출 전용 비밀 키 -> 보안 유지할 때 사용
# INTERNAL_SECRET_KEY = os.getenv("INTERNAL_SECRET_KEY")

# def verify_internal_access(request: Request):
#     secret_key = request.headers.get("X-Internal-Key")
#     if secret_key != INTERNAL_SECRET_KEY:
#         raise HTTPException(status_code=403, detail="Unauthorized access to this endpoint.")
    
# 요청 본문 데이터 모델 정의
class UnblockRequest(BaseModel):
    result: int

@router.post("/lock/unblock/{user_id}")
# async def unblock_sites(user_id: int, request_body: UnblockRequest, request: Request, db: Session = Depends(get_db), _: None = Depends(verify_internal_access)):
async def unblock_sites(user_id: int, request_body: UnblockRequest, db: Session = Depends(get_db)):
    """
    차단 해제 API: 손 모양이 요청된 형태와 일치할 경우 차단된 사이트 해제
    """
    result = request_body.result

    print(f"Received request for user_id: {user_id}, result: {result}")  # 기존 로그

    try:
        # 1. 분석 결과 확인
        if result != 1:  # 1이 아니면 요청 거절 -> 여기서 리다이렉션 페이지로 가도록 수정해야 함
            return JSONResponse(
                status_code=400,
                content={"detail": "손 모양이 요청한 모양과 일치하지 않아서 차단 해제를 진행하지 않았습니다."}
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
        print(f"Error in unblock_sites: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal Server Error: {str(e)}"}
        )

    # finally:
    #     # 업로드된 파일 삭제
    #     if os.path.exists(file_path):
    #         os.remove(file_path)