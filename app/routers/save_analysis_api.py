from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os

router = APIRouter()

class AnalysisResultSchema(BaseModel):
    user_id: int
    timestamp:datetime
    result: int

# 내부 호출 전용 비밀 키 -> 보안 유지할 때 사용
# INTERNAL_SECRET_KEY = os.getenv("INTERNAL_SECRET_KEY")

@router.post("/photo/result")
async def save_analysis_result(data: AnalysisResultSchema):
    try:
        print(f"Received data: {data}")  # 요청 데이터 출력
        user_id = data.user_id
        timestamp = data.timestamp
        result = data.result
    
        print(f"Processing result for user_id: {user_id}, result: {result}")

        unblock_url = f"http://fastapi:8000/lock/unblock/{user_id}"

        async with httpx.AsyncClient() as client:
            print(f"Sending request to unblock_url: {unblock_url} with result: {result}")   
            response = await client.post(
                unblock_url,
                json={"result": result}
                
                # headers={"X-Internal-Key": INTERNAL_SECRET_KEY}  # 내부 호출 전용 토큰 추가
                # json={"result": result, "timestamp": timestamp.isoformat()}
                # timestamp가 필요한 경우 주석 해제
            )

            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content}")

            if response.status_code == 400:
                print(f"[INFO] 400 에러 발생: {response.json().get('detail')}")
                return {
                    "status": "failed",
                    "message": "차단 해제가 거부되었습니다.",
                    "reason": response.json().get("detail"),
                }

            if response.status_code == 500:
                print(f"[ERROR] 500 에러 발생: {response.json().get('detail')}")
                raise HTTPException(status_code=500, detail="서버 내부 에러 발생")
            
            response.raise_for_status()

        print(f"Unblock request successful for user_id: {user_id}")
        return {"status": "success", "message": "Result processed and forwarded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))