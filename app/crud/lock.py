from sqlalchemy.orm import Session
from app.models import Locked, Site

# 차단되어 있는 사이트 목록 조회할 때 사용하는 함수
def get_blocked_sites(db: Session, user_id: int):
    """
    특정 사용자가 차단한 사이트 목록을 반환
    """
    return (
        db.query(Site) # Site 테이블을 기준으로 데이터를 조회
        .join(Locked, Locked.site_id == Site.id) # Lock 테이블과 Site 테이블을 조인
        .filter(Locked.user_id == user_id, Locked.is_deleted == False) # 조인한 결과를 필터링
        .all() # 조회한 데이터를 리스트로 반환
    )

# 차단해제하기 할 때 사용하는 함수
def unblock_sites_by_user(db: Session, user_id: int):
    """
    특정 사용자의 차단 사이트를 DB에서 삭제
    """
    db.query(Locked).filter(Locked.user_id == user_id).delete()
    db.commit()