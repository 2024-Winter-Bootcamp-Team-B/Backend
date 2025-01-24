from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult

router = APIRouter()

@router.get("/task/{task_id}/status")
def get_task_status(task_id: str):
    try:
        task = AsyncResult(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "task_id": task_id,
            "status": task.status,
            "result": task.result if task.ready() else None
        }
    except Exception as e:
        # 예외 처리
        raise HTTPException(status_code=500, detail=f"Error retrieving task status: {str(e)}")