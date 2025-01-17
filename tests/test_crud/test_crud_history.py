from datetime import datetime, timedelta
from app.crud.history import add_history, get_histories, update_history
import pytz

"""
테스트 해야할 것 
1. add_history
2. get_histories
3. update_hisory
"""


def test_add_history(db_session):
    #given
    user_id = 1
    start_time = datetime.now()
    goal_time = start_time + timedelta(hours=1)

    #when
    test_history = add_history(db_session, user_id, start_time, goal_time)

    #then
    assert test_history is not None
    assert test_history.id == user_id 

def test_get_histories(db_session):
    #given
    user_id = 1
    start_time = datetime.now()
    goal_time = start_time + timedelta(hours=1)
    add_history(db_session, user_id, start_time+timedelta(hours=1), goal_time+timedelta(hours=2))
    add_history(db_session, user_id, start_time+timedelta(hours=3), goal_time+timedelta(hours=4))
    
    #when
    histories01 = get_histories(db_session, user_id)
    histories02 = get_histories(db_session, 2)
    #then
    assert len(histories01) == 2 
    assert len(histories02) == 0


def test_update_history(db_session):

    # Given
    test_history01 = add_history(db_session, 1, datetime.now(), datetime.now() + timedelta(hours=1))
    test_history02 = add_history(db_session, 1, datetime.now(), datetime.now() + timedelta(hours=1))

    # 과거 기록 설정
    test_history01.end_time = datetime.now(pytz.timezone("Asia/Seoul"))
    db_session.commit()
    db_session.refresh(test_history01)

    # When
    return_history = update_history(db_session, 1)

    # Then
    assert test_history01.end_time is not None
    assert test_history02.id == return_history.id
    assert test_history02.end_time is not None


