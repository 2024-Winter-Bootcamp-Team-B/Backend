from datetime import datetime, timedelta
import pytz
from sqlalchemy.orm import Session
from app.models import History


# 기록을 추가하기 -> 유저가 서비스를 이용할 때마다 생성
def add_history(db: Session, request_user_id: int, request_start_time : datetime, request_goal_time : datetime):
    new_history = History(
        user_id = request_user_id,
        start_time = request_start_time,
        goal_time = request_goal_time
    )
    db.add(new_history)
    db.commit()

    return new_history

# 유저의 기록 정보를 반환하기
def get_histories(db : Session, request_user_id : int):
    print(f"***** Connected to database: {db.bind.url}")
    return db.query(History).filter(History.user_id == request_user_id).all()

# 차단을 해제하는 시점에 end_time null->현재 시간으로 update 하기
def update_history(db : Session, request_user_id : int):
    
    Blocked_History = db.query(History).filter((History.user_id == request_user_id) & (History.end_time.is_(None))).first()
    
    if Blocked_History :
        Blocked_History.end_time = datetime.now(pytz.timezone("Asia/Seoul"))
        db.commit()
        db.refresh(Blocked_History)
        return Blocked_History
    else :
        return None

def add_history_for_test(db: Session, request_user_id: int, request_start_time : datetime, request_goal_time : datetime):
    new_history = History(
        user_id = request_user_id,
        start_time = request_start_time,
        goal_time = request_goal_time
    )
    db.add(new_history)
    db.commit()
    
    new_history.end_time = datetime.now() + timedelta(hours=3)
    db.commit()
    db.refresh(new_history)
    db.commit()
    return new_history

def get_weekly_histories(db : Session,request_user_id, request_datetime : datetime):
    now = request_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
    one_week_ago = now - timedelta(days=7)

    return db.query(History).filter(
            History.user_id == request_user_id,
            History.start_time >= one_week_ago,  # start_time이 7일 이내인 데이터
            History.start_time <= now,  # start_time이 기준 시간보다 이전인 데이터
            History.end_time.isnot(None)  # 진행중인 건 제외
        ).order_by(History.start_time.asc()).all()