from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter()

class AnalysisResultSchema(BaseModel):
    user_id: int
    timestamp:datetime
    result: int


@router.post("/photo/result")
async def save_analysis_result(data: AnalysisResultSchema):
    try:
        user_id = data.user_id
        timestamp = data.timestamp
        result = data.result

        unblock_url = f"http://fastapi:8000/lock/unblock/{user_id}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                unblock_url,
                json={"result": result, "timestamp": timestamp.isoformat()}
            )
            response.raise_for_status()

        return {"status": "success", "message": "Result processed and forwarded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))