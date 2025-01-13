from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
