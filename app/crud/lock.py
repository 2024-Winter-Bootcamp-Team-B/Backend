from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.crud.history import update_history
from app.crud.site import add_site, site_exist_check
from app.models import Locked, Site

# 차단되어 있는 사이트 목록 조회할 때 사용하는 함수
def get_blocked_sites(db: Session, user_id: int):
    """
    특정 사용자가 차단한 사이트 목록을 반환
    """
    return (
        db.query(Site) # Site 테이블을 기준으로 데이터를 조회
        .join(Locked, Locked.site_id == Site.id) # Locked 테이블과 Site 테이블을 조인
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

    # 해당 사용자의 기록에 end_time 추가
    update_history(db, user_id)

# 차단할 떄 사용하는 함수
def add_block_sites(
        db : Session, 
        request_user_id : int, 
        request_siteURL : List[str],
        request_goal_time : datetime):
    
    for site in request_siteURL : 
        
        # 차단 기록이 있는 사이트인지 체크
        is_exist = site_exist_check(db, site)

        if is_exist : # 차단 기록 O

            # 차단  횟수 ++
            is_exist.blocked_cnt += 1
            db.commit()

        else : # 차단 기록 X
            # 새로운 사이트를 추가하기
            is_exist = add_site(db, site)
        
        # 요청 사이트를 차단하기
        add_locked(db, request_user_id, is_exist.id, request_goal_time)

# 진짜 디비에 차단하기
def add_locked(db : Session, request_user_id : int, request_site_id : int, request_goal_time : datetime):
    new_lock = Locked(
                user_id = request_user_id,
                site_id = request_site_id,
                goal_time = request_goal_time
            )
    db.add(new_lock)
    db.commit()
    return new_lock
