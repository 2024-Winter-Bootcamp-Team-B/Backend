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
from app.routers.image_api import router as image_router
from app.routers.history_api import router as history_router
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

init_db()