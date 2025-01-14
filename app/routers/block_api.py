from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from app.database import SessionLocal
from sqlalchemy.orm import Session

from app.models import History, Lock, Site

router = APIRouter()

# DB 세션 종속성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/lock/block")
async def post_lock_sites(request: Request, db: Session = Depends(get_db)):
    """
        {
            "user_id": "hello",
            "start_time": "2023-02-26T15:12:17.536Z",
            "goal_time": "2023-02-26T15:50:17.536Z"
            "sites": [
                "https://example.com",
                "https://test.com",
                "https://mywebsite.org"
            ]
        }
    """
    try:
        

        # 요청에서 JSON 데이터 추출
        data = await request.json()
        user_id_request = data.get("user_id")

        iso_format = "%Y-%m-%dT%H:%M:%S.%fZ"  # ISO 8601 포맷
        general_format = "%Y-%m-%d %H:%M:%S"  # 일반적인 출력 포맷

        start_time = datetime.strptime(data["start_time"], iso_format).strftime(general_format)
        goal_time = datetime.strptime(data["goal_time"], iso_format).strftime(general_format)
        
        sites = data.get("sites")

        for site in sites:
            # 사이트 확인
            is_exist = db.query(Site).filter(Site.url == site).first()

            if is_exist:
                is_exist.blocked_cnt += 1
                db.commit()
                
                # Lock 객체 추가
                new_lock = Lock(
                    user_id=user_id_request,
                    site_id=is_exist.id,
                    goal_time=goal_time,
                )
                db.add(new_lock)

            else:
                # 새로운 사이트 추가
                new_site = Site(
                    url=site,
                    blocked_cnt=1,
                )
                db.add(new_site)
                db.commit()  
                db.refresh(new_site)

                new_lock = Lock(
                    user_id=user_id_request,
                    site_id=new_site.id,
                    goal_time=goal_time,
                )
                db.add(new_lock)


        new_history = History(
            user_id = user_id_request,
            start_time = datetime.strptime(data["start_time"], iso_format),
            goal_time = datetime.strptime(data["goal_time"], iso_format)
        )
        db.add(new_history)

        db.commit()
        # 성공 응답 반환
        return JSONResponse(
            status_code=200,
            content={
                "message": "Data processed successfully",
                "data": {
                    "user_id": user_id_request,
                    "start_time": start_time,
                    "goal_time": goal_time,
                    "sites" : sites
                },
            },
        )

    except Exception as e:
        # 예외 발생 시 에러 응답
        print(f"Error: {str(e)}")  # 디버깅 출력
        return JSONResponse(
            status_code=500,
            content={"message": f"Internal Server Error: {str(e)}"},
        )
