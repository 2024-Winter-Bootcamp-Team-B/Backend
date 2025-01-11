'''
FastAPI애플리케이션의 진입점. 라우터를 등록하고 서버를 실행한다
FastAPI인스턴스를 생성하고, 라우터를 등록하며 애플리케이션을 설정한다
'''
# EX>

from fastapi import FastAPI
from models import *

app.include_router(user.router, prefix="/users")
app.include_router(chat.router, prefix="/ws")
app.include_router(mentor.router, prefix="/mentors")
app.include_router(chatroom.router, prefix="/chatrooms")
app.include_router(prescription.router, prefix="/prescriptions")
app.include_router(root.router, prefix="")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(_: str = Depends(root.get_admin)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)
