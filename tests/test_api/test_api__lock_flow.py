from datetime import datetime, timedelta
import pytest

from fastapi.testclient import TestClient
from app.crud.history import *
from app.crud.lock import get_blocked_sites
from app.crud.user import add_user, get_user_by_id
from app.main import app
from tests.conftest import reset_database

client = TestClient(app)

@pytest.mark.order(1)
def test_most_locked_site_v1(db_session):
    reset_database(db_session)
    """
    누적 차단 횟수 많은 사이트 API :아무런 정보가 없을 때 (최초에) 가장 많이 차단된 사이트를 요구할 때
    """
    #given
    test_user = add_user(db_session,"test01", "test01", "test_name", "example@naver.com")
    #when
    response = client.get(f"/lock/most-blocked")
    print("Response JSON:", response.json())  # 전체 응답 JSON 출력
    print("Result:", response.json()["result"]) 
    #then
    assert test_user is not None
    assert response.status_code == 200
    assert response.json()["result"] == "차단되었던 사이트 기록이 없습니다."


@pytest.mark.order(2)
def test_user_block(db_session):
    """
    차단하기 API 테스트 
    """
    #given
    test_user = get_user_by_id(db_session,1)
    #when  
    #사이트를 차단하자
    response = client.post(
        "/lock/block", 
        json={
            "user_id": test_user.id,
            "start_time": "2023-02-26T15:12:17.536Z",
            "goal_time": "2023-02-26T15:50:17.536Z",
            "sites": [
            "https://example.com",
            "https://test.com",
            "https://mywebsite0.org",
            "https://mywebsite1.org",
            "https://mywebsite2.org",
            "https://mywebsite25.org"
            ]
        }
    )
    #then
    assert response.status_code == 200
    assert response.json()["message"] == "Data processed successfully"





@pytest.mark.order(3)
def test_user_blocked_sites(db_session):
    """
    특정 사용자가 차단한 사이트 목록을 반환 API
    """
    #given
    request_test_user_id = 1
    sites = get_blocked_sites(db_session, request_test_user_id)
    #when
    response = client.get(f"/lock/blocked-site/{request_test_user_id}")
    #then
    assert response.status_code == 200
    assert response.json()["user_id"] == request_test_user_id
    assert sites is not None


@pytest.mark.order(4)
def test_user_history(db_session):
    """
    특정 유저의 정보 가져오기 
    """
    #given
    now = datetime.now()  # 테스트 기준 날짜
    one_week_ago = now - timedelta(days=7)
    test_user = get_user_by_id(db_session,1)
    request_test_user_id = test_user.id
    test_history01 = add_history_for_test(db_session, request_test_user_id, one_week_ago + timedelta(days=1), one_week_ago + timedelta(days=1, hours=3))
    test_history02 = add_history_for_test(db_session, request_test_user_id, one_week_ago + timedelta(days=2), one_week_ago + timedelta(days=2, hours=3))

    #when
    response = client.get(f"/statistic/{request_test_user_id}")
    result_stat = response.json()
    #then
    assert test_history01 is not None
    assert test_history02 is not None
    assert result_stat.get("message") == "성공"
