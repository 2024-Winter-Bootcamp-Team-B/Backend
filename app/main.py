'''
FastAPI애플리케이션의 진입점. 라우터를 등록하고 서버를 실행한다
FastAPI인스턴스를 생성하고, 라우터를 등록하며 애플리케이션을 설정한다
'''
# EX>

# from fastapi import FastAPI
# from models import *

# app.include_router(user.router, prefix="/users")
# app.include_router(chat.router, prefix="/ws")
# app.include_router(mentor.router, prefix="/mentors")
# app.include_router(chatroom.router, prefix="/chatrooms")
# app.include_router(prescription.router, prefix="/prescriptions")
# app.include_router(root.router, prefix="")

# @app.get("/openapi.json", include_in_schema=False)
# async def openapi(_: str = Depends(root.get_admin)):
#     return get_openapi(title=app.title, version=app.version, routes=app.routes)



from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routers.image_api import router as image_router
from app.routers.history_api import router as history_router
from app.routers.blockedSiteCheck_api import router as blocked_site_router
from app.routers.site_api import router as site_router
from app.routers.login_api import router as login_router
from app.routers.block_api import router as block_router


from app.models import Base
from app.database import engine
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os

# 데이터베이스 테이블 생성
def init_db():
    Base.metadata.create_all(bind=engine)
    print("데이터베이스 테이블이 생성되었습니다.")



app = FastAPI()


# .env에서 SECRET_KEY 가져오기
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY is not set in the environment variables.")
# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key=secret_key)
# 정적 파일 제공
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 사용자가 이미지를 입력하면 그 이미지를 서버에 업로드하고, 
# mediapipe를 사용하여 요청된 이미지와 동일한 이미지를 업로드 했는지 확인 후
# 결과를 반환하는 API를 구현하세요.

# 라우터 등록
app.include_router(image_router)
app.include_router(history_router)
app.include_router(blocked_site_router, prefix="/lock", tags=["Blocked Sites"])
app.include_router(site_router)
app.include_router(login_router)
app.include_router(block_router)

@app.get("/index", response_class=HTMLResponse)
async def serve_index():
    # HTML 파일 경로 설정
    file_path = os.path.join("app", "templates", "index.html")
    if not os.path.exists(file_path):
        return HTMLResponse(content="File not found", status_code=404)
    
    # HTML 파일 읽기
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

init_db()