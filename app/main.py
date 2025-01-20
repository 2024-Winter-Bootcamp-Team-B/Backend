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
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base
from app.database import engine
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 데이터베이스 초기화 함수
def init_db():
    """데이터베이스 테이블을 초기화합니다."""
    Base.metadata.create_all(bind=engine)
    print("데이터베이스 테이블이 생성되었습니다.")

# FastAPI 애플리케이션 생성
app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
    # 더 추가할 수 있음, 나중에 우리 도메인 추가할 예정
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 미들웨어 추가
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY is not set in the environment variables.")
app.add_middleware(SessionMiddleware, secret_key=secret_key)

# 정적 파일 제공
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 라우터 등록
app.include_router(site_router, tags=["Login"])
app.include_router(login_router, tags=["Login"])
app.include_router(block_router, tags=["Block"])
app.include_router(blocked_site_router, prefix="/lock", tags=["Blocked Sites Check"])
app.include_router(image_router, tags=["Image"])
app.include_router(analysis_router, tags=["Analysis"])
app.include_router(unblock_router, tags=["Blocked Sites Clear"])
app.include_router(history_router, tags=["History"])

# HTML 파일을 반환하는 엔드포인트
@app.get("/index", response_class=HTMLResponse)
async def serve_index():
    file_path = os.path.join("app", "templates", "index.html")
    if not os.path.exists(file_path):
        return HTMLResponse(content="File not found", status_code=404)
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# 데이터베이스 초기화 (테스트 환경 제외)
if os.getenv("TESTING") != "TRUE":
    init_db()