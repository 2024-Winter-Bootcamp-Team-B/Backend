
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from app.database import SessionLocal
from app.models import Site
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

@router.get("/lock/blocked-site/most")
async def get_most_site(db: Session = Depends(get_db)):
    try :
        sites = db.query(Site).order_by(desc(Site.blocked_cnt)).limit(5).all()
        return JSONResponse(
            status_code=200,  # HTTP 상태 코드 200을 명시
            content={"result": [site.url for site in sites]}
        )      

    except Exception as e :
        return JSONResponse(
            status_code=500,
            content={"message" : f"Internal Server Error : {str(e)}"}
        )