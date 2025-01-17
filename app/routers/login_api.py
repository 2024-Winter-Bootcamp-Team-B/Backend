#login_api.py
from datetime import datetime
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth

from starlette.config import Config
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from app.crud.user import add_user, get_user_by_email, get_user_by_id
from app.database import get_db  # DB 세션 가져오기
from app.models import User

import os
import httpx
# 환경 변수 로드
load_dotenv()

# FastAPI Router 초기화
router = APIRouter()

# Authlib 설정
config = Config(environ=os.environ)
oauth = OAuth(config)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# 기본 Redirect URI 설정 (환경 변수 미설정 시)
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# Google 로그인 엔드포인트
@router.get("/auth/login")
async def login_with_google(request: Request):
    redirect_uri = "http://localhost:8000/auth/callback"
    print(f"Redirecting to Google with URI: {redirect_uri}")  # 디버깅 출력
    return await google.authorize_redirect(request, redirect_uri)


# Google 로그인 콜백 엔드포인트
@router.get("/auth/callback")
async def auth_callback(request: Request):
    """
    Google OAuth 콜백 처리
    """
    try:
        # 액세스 토큰 발급
        token = await google.authorize_access_token(request)
        if not token:
            raise HTTPException(status_code=400, detail="Failed to fetch access token.")
        # 사용자 정보 요청
        user_info = await google.get("userinfo", token=token)
        user_data = user_info.json()

        return JSONResponse(
            status_code=200,
            content={
                "message": "Google Login Successful",
                "user": user_data,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during callback: {str(e)}")


# Google ID 토큰 검증 엔드포인트
@router.post("/auth/google-token")
async def handle_google_token(request: Request, db: Session = Depends(get_db)):
    """
    클라이언트에서 전달된 ID 토큰을 검증
    """
    try:
        # 요청으로부터 토큰 추출
        data = await request.json()
        token = data.get("token")
        if not token:
            raise HTTPException(status_code=400, detail="No token provided.")

        # Google API를 사용하여 ID 토큰 검증
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://oauth2.googleapis.com/tokeninfo",
                params={"id_token": token},
            )
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Invalid token.")
            
            # 사용자 정보 파싱
            user_info = response.json()
        
        user = get_user_by_email(db, user_info["email"])

        
        if not user : # 처음 온 회원
            add_user(db,user_info.get("email"), user_info.get("name"))


        # 세션에 정보 저장
        request.session["user_id"] = user.id
        request.session["user_email"] = user.email

        return JSONResponse(
            status_code=200,
            content={
                "message": "Token verified",
                "user": user_info,
                "email" : user_info.get("email"),
                "name" : user_info.get("name"),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying token: {str(e)}")


@router.get("/user/info")
async def get_current_user(request : Request, db : Session=Depends(get_db)):
    session_user_id = request.session.get("user_id")
    
    # 로그인 X 유저
    if not session_user_id :
        raise HTTPException(status_code=401, detail="User not logged in")
    
    logged_in_user = get_user_by_id(db, session_user_id)

    # 유저를 찾을 수 없을 때
    if not logged_in_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    return JSONResponse(
        status_code=200,
        content={
            "user_id" : logged_in_user.id,
            "email" : logged_in_user.email,
            "name" : logged_in_user.user_name
        }
    )

@router.post("/auth/logout")
async def logout(request : Request):
    request.session.clear()

    return JSONResponse(
        status_code=200,
        content={
            "message" : "Successfully logged out"
        }
    )