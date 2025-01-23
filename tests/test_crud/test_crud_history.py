import pytz

from datetime import datetime, timedelta
from app.database import Base
from tests.conftest import reset_database
from app.crud.history import *

def test_add_history(db_session):
    reset_database(db_session,Base.metadata)
    #given
    test_user_id = 1
    test_start_time = datetime.now()
    test_goal_time = datetime.now() + timedelta(hours=1)

    #when
    test_history = add_history(db_session, test_user_id, test_start_time, test_goal_time)

    #then
    assert test_history is not None
    assert test_history.end_time is None
    assert test_history.user_id == test_user_id

# def test_get_histories(db_session):
#     reset_database(db_session,Base.metadata)
#     #given
#     user_id = 1
#     start_time = datetime.now()
#     goal_time = start_time + timedelta(hours=1)
#     add_history(db_session, user_id, start_time+timedelta(hours=1), goal_time+timedelta(hours=2))
#     add_history(db_session, user_id, start_time+timedelta(hours=3), goal_time+timedelta(hours=4))

#     #when
#     histories01 = get_histories(db_session, user_id)
#     histories02 = get_histories(db_session, 2)
#     #then
#     assert len(histories01) == 2 
#     assert len(histories02) == 0


def test_update_history(db_session):
    reset_database(db_session,Base.metadata)
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

def test_weekly_history(db_session):
    reset_database(db_session, Base.metadata)
    start = datetime.now() 

    #given
    thu = add_history_for_test(db_session, 1, start - timedelta(days=6), start -timedelta(days=6) + timedelta(hours=1))
    fri = add_history_for_test(db_session, 1, start - timedelta(days=5), start -timedelta(days=5) + timedelta(hours=1))
    sat = add_history_for_test(db_session, 1, start - timedelta(days=4), start -timedelta(days=4) + timedelta(hours=1))
    sun = add_history_for_test(db_session, 1, start - timedelta(days=3), start -timedelta(days=3) + timedelta(hours=1))
    mon = add_history_for_test(db_session, 1, start - timedelta(days=2), start -timedelta(days=2) + timedelta(hours=1))
    tue = add_history_for_test(db_session, 1, start - timedelta(days=1), start -timedelta(days=1) + timedelta(hours=1))
    wen = add_history_for_test(db_session, 1, start - timedelta(hours=1), start + timedelta(hours=1))

    #when
    test_weekly = get_weekly_histories(db_session, start)
    #then
    assert thu is not None
    assert thu.end_time is not None
    assert len(test_weekly) == 7



