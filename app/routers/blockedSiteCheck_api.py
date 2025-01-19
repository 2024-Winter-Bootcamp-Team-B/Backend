
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.lock import get_blocked_sites
from app.schemas import BlockedSitesResponse

router = APIRouter()

@router.get("/blocked-site/{user_id}", response_model=BlockedSitesResponse)
def read_blocked_sites(user_id: int, db: Session = Depends(get_db)):
    """
    특정 사용자가 차단한 사이트 목록을 반환
    """
    # 데이터베이스에서 차단된 사이트 조회
    sites = get_blocked_sites(db, user_id)
    
    if not sites:
        return JSONResponse(
            status_code=200,
            content={
                "message": "차단된 사이트 없음"
            }
        )
    
    # 응답 생성
    
    return JSONResponse(
            status_code=200,
            content={
                "message": "성공",
                "user_id" : user_id,
                "sites" : [site.url for site in sites]
            }
        )