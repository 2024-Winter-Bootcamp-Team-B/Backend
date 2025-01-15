
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from app.crud.site import get_most_blocked_site
from app.database import get_db
from app.models import Site
from sqlalchemy.orm import Session

router = APIRouter()

# 가장 많이 차단되어 있는 상위 5개의 사이트 반환해주기
@router.get("/lock/most-blocked")
async def most_site(db: Session = Depends(get_db)):
    try :
        sites = get_most_blocked_site(db)
        if sites :
            return JSONResponse(
                status_code=200,  # 차단 사이트 기록이 하나라도 있는 경우 -> { "result" : ["example1.com", "example2.com"]}
                content={"result": [site.url for site in sites]}
            )
        else : 
            return JSONResponse( # 초기에 차단 사이트 기록이 없는데 상위 5개를 요청할 떄
                status_code=200, 
                content={"result": "차단되었던 사이트 기록이 없습니다."}
            )  

    except Exception as e :
        return JSONResponse(
            status_code=500,
            content={"message" : f"Internal Server Error : {str(e)}"}
        )