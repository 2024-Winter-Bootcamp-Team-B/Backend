from sqlalchemy.orm import Session
from app.models import Lock, Site

def get_blocked_sites(db: Session, user_id: int):
    return (
        db.query(Site) # Site 테이블에서 데이터를 조회하기 위한 쿼리를 시작 
        .join(Lock, Lock.site_id == Site.id) # Lock.site_id와 Site.id가 같을 때 두 테이블의 데이터를 연결
        .filter(Lock.user_id == user_id, Lock.is_deleted == False)
        # Lock 테이블에서 user_id가 함수에 전달된 사용자 ID와 일치하는 데이터를 찾음.
        # Lock 테이블에서 삭제되지 않은(is_deleted == False) 차단 기록만 가져옴
        .all() 
        # 쿼리를 실행하고 조건에 맞는 모든 결과를 리스트로 반환
    )