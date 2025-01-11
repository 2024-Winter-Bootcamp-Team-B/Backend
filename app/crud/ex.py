from sqlalchemy.orm import Session
from app.models import User_Test
from app.schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User_Test(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User_Test).filter(User_Test.id == user_id).first()

# feat/#10 : 통계정보 가져오기
def get_user_history(db : Session, user_id : int):

