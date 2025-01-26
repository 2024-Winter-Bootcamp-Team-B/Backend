# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.crud.lock import get_blocked_sites
# from app.schemas import BlockedSitesResponse

# router = APIRouter()

# @router.get("/blocked-site/{user_id}", response_model=BlockedSitesResponse)
# def read_blocked_sites(user_id: int, db: Session = Depends(get_db)):
#     """
#     특정 사용자가 차단한 사이트 목록을 반환
#     """
#     # 데이터베이스에서 차단된 사이트 조회
#     sites = get_blocked_sites(db, user_id)
    
#     # 차단된 사이트가 없으면 404 에러 반환
#     if not sites:
#         raise HTTPException(status_code=404, detail="No blocked sites found for this user")
    
#     # 응답 생성
#     return {
#         "user_id": user_id,
#         "blocked_sites": [{"url": site.url} for site in sites] # 차단된 사이트 목록을 반환하도록 수정함
#     }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.lock import get_blocked_sites

router = APIRouter()

@router.get("/blocked-site/{user_id}")
def read_blocked_sites(user_id: int, db: Session = Depends(get_db)):
    """
    특정 사용자가 차단한 사이트 목록을 반환
    """
    # 데이터베이스에서 차단된 사이트 조회
    sites = get_blocked_sites(db, user_id)
    
    # 차단된 사이트가 없으면 404 에러 반환
    if not sites:
        raise HTTPException(status_code=404, detail="No blocked sites found for this user")
    
    # 응답 생성
    return {
        "message": "Data processed successfully",
        "user_id": user_id,
        "sites": [site.site.url.replace("https://", "").replace("http://", "") for site in sites]
        # sites 필드는 URL의 프로토콜(https://, http://)을 제거하고 도메인만 반환하도록 처리
    }