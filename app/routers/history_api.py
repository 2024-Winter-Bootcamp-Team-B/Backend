from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.services.statistic_service import *
from app.crud.history import *
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/statistic/{request_user_id}")
async def user_statistic(request_user_id: int, db: Session = Depends(get_db)):
    
    try :
        now = datetime.now()
        # 디비에서 찾아옴 
        histories = get_weekly_histories(db, request_user_id, now)
        
        
        # 기록이 없을 경우
        if not histories:
            return JSONResponse(
                status_code=200,
                content={"message": "기록이 없습니다."}
                
            )

        # 결과 데이터 구성
        result_stat = get_stat_result(histories, now)
        
        result = [
            {
                "date": stat.date,
                "goal": stat.goal,
                "actual" : stat.actual
            }
            for stat in result_stat
        ]
        # 성공 응답 반환
        return JSONResponse(
            status_code=200,
            content={
                "message": "성공",
                "result": result
            }
        )

    except Exception as e :
        return JSONResponse(
            status_code=500,
            content={"message" : f"Internal Server Error : {str(e)}"}
        )
    