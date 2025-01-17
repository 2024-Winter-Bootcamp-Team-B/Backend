from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models import User

def get_user_by_email(db : Session, request_email : str):
    return db.query(User).filter(User.email == request_email).first()

def add_user(db : Session,
            request_login_id : str, request_login_password :str,
            request_user_name : str, request_email : str):
    new_user = User(
        login_id = request_login_id,
        login_password = request_login_password,
        email = request_email,
        user_name = request_user_name,
    )
    db.add(new_user)
    db.commit()
    return new_user

def get_user_by_id(db : Session, request_id : int):
    return db.query(User).filter(User.id==request_id).first()

def check_exist_by_login_id(db : Session, request_login_id : str):
    return db.query(User).filter(User.login_id == request_login_id).first()

def login_process(db : Session, request_login_id : str, request_login_password : str):
    return db.query(User).filter(and_(User.login_id == request_login_id, User.login_password == request_login_password)).first()