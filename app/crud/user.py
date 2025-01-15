from datetime import datetime
from sqlalchemy.orm import Session
from app.models import User

def get_user_by_email(db : Session, request_email : str):
    return db.query(User).filter(User.email == request_email).first()

def add_user(db : Session, request_email : str, request_user_name : str):
    new_user = User(
        email = request_email,
        name = request_user_name,
    )
    db.add(new_user)
    db.commit()
    return new_user