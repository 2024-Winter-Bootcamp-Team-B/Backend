import pytz

from datetime import datetime, timedelta
from app.database import Base
from tests.conftest import reset_database
from app.crud.history import *

def test_add_history(db_session):
    reset_database(db_session)
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

def test_get_weekly_histories(db_session):
    reset_database(db_session)
    
    # given
    user_id = 1
    now = datetime.now()  # 테스트 기준 날짜
    one_week_ago = now - timedelta(days=7)
        # 데이터 추가
    add_history_for_test(db_session, user_id, one_week_ago + timedelta(days=1), one_week_ago + timedelta(days=1, hours=3))
    add_history_for_test(db_session, user_id, one_week_ago + timedelta(days=2), one_week_ago + timedelta(days=2, hours=3))
        # 7일 넘은 데이터
    add_history_for_test(db_session, user_id, one_week_ago + timedelta(days=8), one_week_ago + timedelta(days=8, hours=3))

    # when
    histories01 = get_weekly_histories(db_session, user_id, now)  # 유효한 기간 내 데이터
    histories02 = get_weekly_histories(db_session, 2, now)  # 없는 사용자

    # then
    assert len(histories01) == 2  # 7일 이내 데이터만 포함
    assert len(histories02) == 0  # user_id=2는 데이터 없음


def test_update_history(db_session):
    reset_database(db_session)
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
    reset_database(db_session)
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
    test_weekly = get_weekly_histories(db_session, 1, start)
    #then
    assert thu is not None
    assert thu.end_time is not None
    assert len(test_weekly) == 7


