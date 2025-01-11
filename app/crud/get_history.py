# feat/#10 : 통계정보 가져오기
from app.models import History

def get_user_history(db : Session, user_id : int):
    return db.query(History).filter(History.user_id == user_id).all()
