from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routers.image_api import router as image_router
from app.routers.history_api import router as history_router
from app.routers.blockedSiteCheck_api import router as blocked_site_router
from app.routers.site_api import router as site_router
from app.routers.login_api import router as login_router
from app.routers.block_api import router as block_router
from app.routers.unblock_api import router as unblock_router
from app.routers.save_analysis_api import router as analysis_router
from app.routers.task_id_api import router as task_id_router
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import engine, Base
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os

# 데이터베이스 테이블 생성
def init_db():
    Base.metadata.create_all(bind=engine)
    print("데이터베이스 테이블이 생성되었습니다.")

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "chrome-extension://klhjebgdjainkellmacilgichiddfeod",  # Chrome 확장 프로그램의 Origin 추가
    "https://www.focus-on-site.com",
    "https://server.focus-on-site.com",

    # 더 추가할 수 있음, 나중에 우리 도메인 추가할 예정
]

# FastAPI와 React는 다른 도메인에서 실행되기 때문에, CORS (Cross-Origin Resource Sharing) 설정을 해줘야 함
# (FastAPI = 8000번 포트, React = 5173번 포트)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Instrumentator().instrument(app).expose(app)

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
# 결과를 반환하는 API를 구현

# 라우터 등록
app.include_router(site_router, tags=["Login"])
app.include_router(login_router, tags=["Login"])

app.include_router(block_router, tags=["Block"])

app.include_router(blocked_site_router, prefix="/lock", tags=["Blocked Sites Check"])

app.include_router(image_router, tags=["Image"])

app.include_router(analysis_router, tags=["Analysis"])

app.include_router(unblock_router, tags=["Blocked Sites Clear"])

app.include_router(history_router , tags=["History"])

app.include_router(task_id_router, tags=["Task ID"])



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