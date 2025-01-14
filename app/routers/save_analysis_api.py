from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/photo/result")
async def save_analysis_result(data: int):
    try:
        result = data.get("result")

        # 결과를 저장하거나 처리
        print(f"Analysis Result: {result}")

        return {"status": "success", "message": "Result saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
