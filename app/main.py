from fastapi import FastAPI
from app.routers.image_api import router as image_router
from app.routers.history_api import router as history_router
from app.routers.blockedSiteCheck_api import router as blocked_site_router
from app.models import Base
from app.database import engine


# 데이터베이스 테이블 생성
def init_db():
    Base.metadata.create_all(bind=engine)
    print("데이터베이스 테이블이 생성되었습니다.")



app = FastAPI()

# 사용자가 이미지를 입력하면 그 이미지를 서버에 업로드하고, 
# mediapipe를 사용하여 요청된 이미지와 동일한 이미지를 업로드 했는지 확인 후
# 결과를 반환하는 API를 구현하세요.

# 라우터 등록
app.include_router(image_router)
app.include_router(history_router)
app.include_router(blocked_site_router, prefix="/lock", tags=["Blocked Sites"])


init_db()