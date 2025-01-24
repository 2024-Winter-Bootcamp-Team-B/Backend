from datetime import datetime
from fastapi.testclient import TestClient
import pytest

from app.crud.lock import *
from app.crud.site import *
from app.crud.user import *
from app.main import app
from tests.conftest import reset_database


client = TestClient(app)

@pytest.mark.order(1)
def test_setting_lock_data(db_session):
    """
    unlock flow 테스트
    """
    reset_database(db_session)

    #given
        #User
    test_user = add_user(db_session,"test01", "test01", "test_name", "example@naver.com")
        #Locked
    test_sites = ["youtube.com","instagram.com"]
    test_locked = add_block_sites(db_session, test_user.id, test_sites, datetime.now())

    #then
    assert test_user is not None
    assert test_user.id == 1
    assert test_locked is not None
    assert len(test_locked) == 2


@pytest.mark.order(2)
def test_uplockflow():
    #given
    test_user_id = 1
    test_image_path = "image/11111.jpg"
    test_hand_shape = "[1, 0, 1, 1, 0]"  # 예: JSON 문자열로 손 모양 값 전달

    #when
    try :
        with open(test_image_path, "rb") as test_image :
            response = client.post(
                "/lock/upload-image",
                data = {
                    "user_id" : test_user_id,
                    "hand_shape": test_hand_shape  # hand_shape 추가
                },
                files = {"file" : ("11111.jpg", test_image, "image/jpeg")}
            )
            # 상태 코드 출력
            print("Status Code at unlock - TESTING :", response.status_code)
            response_json = response.json()
            # JSON 응답 출력
            try:
                print("Response JSON at unlock - TESTING :", response.json())
            except Exception as e:
                print("Error parsing JSON response at unlock - TESTING :", str(e))
    except FileNotFoundError :
        print("파일 못 찾는다")
        
    #then
    assert "message" in response_json
    assert response_json["message"] == "File uploaded and analysis started"

    assert "file_path" in response_json
    assert "task_id" in response_json