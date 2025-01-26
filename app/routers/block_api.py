from datetime import datetime, timedelta
from fastapi import APIRouter,Depends, Request
from fastapi.responses import JSONResponse
from app.crud.lock import add_block_sites
from app.crud.history import add_history
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# str으로 받은 거 db에 넣을 수 있게 포맷하는 함수
def date_format(time: str, type: bool):
    iso_format = "%Y-%m-%dT%H:%M:%S.%fZ"  # ISO 8601 포맷

    
    # 문자열을 datetime 객체로 변환
    date = datetime.strptime(time, iso_format) + timedelta(hours=9)
    
    if type == True:
        return date
    return f"{date}"


@router.post("/lock/block")
async def post_lock_sites(request: Request, db: Session = Depends(get_db)):
    try:
        
        # 요청에서 JSON 데이터 추출
        data = await request.json()
        request_user_id = data.get("user_id")
        request_sites = data.get("sites")

        # 사이트 차단하기
        add_block_sites(db, request_user_id, request_sites, date_format(data["goal_time"], True))
        # 차단 기록 남기기
        add_history(db, request_user_id, date_format(data["start_time"], True), date_format(data["goal_time"], True))


        ## 자바 스크립트 ... 
    

        # 성공 응답 반환
        return JSONResponse(
            status_code=200,
            content={
                "message": "Data processed successfully",
                "data": {
                    "user_id": request_user_id,
                    "start_time": date_format(data["start_time"], False),
                    "goal_time": date_format(data["goal_time"], False),
                    "sites" : request_sites
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
