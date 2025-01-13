# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.crud import user as crud_user
# from app.schemas import UserCreate, UserResponse
# from app.database import get_db

# router = APIRouter()

# @router.post("/users/", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     return crud_user.create_user(db, user)

# @router.get("/users/{user_id}", response_model=UserResponse)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     return crud_user.get_user(db, user_id)
