from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models import  Site

# 차단 빈도 수 상위 5개 사이트 추출 
def get_most_blocked_site(db: Session):
    return db.query(Site).order_by(desc(Site.blocked_cnt)).limit(5).all()


# 차단 기록이 있는 사이트인지 체크하는 함수
def site_exist_check(db: Session, request_siteUrl : str):
    site = db.query(Site).filter(Site.url == request_siteUrl).first()
    print(f"Checking site existence: {request_siteUrl} -> {'Found' if site else 'Not Found'}")
    return site

# 차단 기록이 없으면 디비에 추가하기
def add_site(db : Session, request_siteURL : str):
    new_site = Site(
                url = request_siteURL,
                blocked_cnt = 1
            )
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return new_site

def all_site(db : Session):
    return db.query(Site).all()