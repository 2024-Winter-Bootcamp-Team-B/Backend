from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.models import History
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/statistic/{user_id}")
async def get_histories(user_id: str):
    print("statistic")
    """
    사용자의 통계 정보를 반환
    [예시] 
    [
        {
            "message": "성공",
            "user_id": 1,
            "start_time": "2023-01-11T10:00:00",
            "goal_time": "2023-01-11T11:00:00",
            "end_time": null
        },
        {
            "message": "성공",
            "user_id": 1,
            "start_time": "2023-01-11T12:00:00",
            "goal_time": "2023-01-11T13:00:00",
            "end_time": "2023-01-11T12:45:00"
        }
    ]
    """
    try :
        # 디비에서 찾아옴 
        # histories = db.query(History).filter(History.user_id == user_id).all()
        histories = [
            {
                "user_id": user_id,
                "start_time": datetime(2023, 1, 11, 10, 0, 0),
                "goal_time": datetime(2023, 1, 11, 10, 0, 0),
                "end_time": None,
            },
            {
                "user_id": user_id,
                "start_time": datetime(2023, 1, 11, 10, 0, 0),
                "goal_time": datetime(2023, 1, 11, 10, 0, 0),
                "end_time": datetime(2023, 1, 11, 10, 0, 0),
            },
        ]

        # 사용자의 기록이 없는 경우
        if not histories:
            return JSONResponse(
                status_code=400,
                content={
                    "message" : "실패"
                }
            )
        result = [
            {
                "message": "성공",
                "userID": user_id,
                "startTime": history["start_time"],  
                "endTime": history["end_time"],
                "goalTime": history["goal_time"],
            }
            for history in histories 
        ]
        return result

    except Exception as e :
        return JSONResponse(
            status_code=500,
            content={"message" : f"Internal Server Error : {str(e)}"}
        )
    