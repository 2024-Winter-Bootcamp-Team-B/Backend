from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.database import SessionLocal
from app.models import History
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

@router.get("/statistic/{user_id}")
async def get_histories(user_id: int, db: Session = Depends(get_db)):
    
    try :
        # 디비에서 찾아옴 
        histories = db.query(History).filter(History.user_id == user_id).all()

        
        # 기록이 없을 경우
        if not histories:
            return JSONResponse(
                status_code=200,
                content={"message": "기록이 없습니다."}
            )

        # 결과 데이터 구성
        result = [
            {
                "user_id": history.user_id,
                "start_time": history.start_time.isoformat(),  # datetime -> 문자열로 변환
                "end_time": history.end_time.isoformat() if history.end_time else None,
                "goal_time": history.goal_time.isoformat(),
            }
            for history in histories
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
    