from sqlalchemy.orm import Session
from app.models import Lock, Site

def get_blocked_sites(db: Session, user_id: int):
    """
    특정 사용자가 차단한 사이트 목록을 반환
    """
    return (
        db.query(Site) # Site 테이블을 기준으로 데이터를 조회
        .join(Lock, Lock.site_id == Site.id) # Lock 테이블과 Site 테이블을 조인
        .filter(Lock.user_id == user_id, Lock.is_deleted == False) # 조인한 결과를 필터링
        .all() # 조회한 데이터를 리스트로 반환
    )