"""
테스트 해야할 것 
1. user_sign_up(request : Request, db : Session = Depends(get_db))
2. user_login(request : Request, db : Session = Depends(get_db))

"""

"""
def test_create_user(client):
    test_nickname = "test_nickname"
    response = client.post(
        "/users",
        json={"nickname": test_nickname},
    )
    assert response.status_code == 200
    assert response.json()["nickname"] == test_nickname"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

def test_user_sign_up():
    #given
    test_login_id = "test"
    test_login_password = "test"
    test_user_name = "test_user"
    test_user_email = "test@example.com"

    #when
    response = client.post(
        "/user/sign-up", 
        json={
            "login_id" : test_login_id,
            "login_password" : test_login_password,
            "name" : test_user_name, 
            "email" : test_user_email
        }
    )

    #then 
    assert response.status_code == 200
    assert response.json()["message"] == "성공"

def test_user_login():
    #given
    test_login_id = "test"
    test_login_password = "test"

    #when
    response = client.post(
        "/user/login-g", 
        json={
            "login_id" : test_login_id,
            "login_password" : test_login_password
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "성공"
    assert response.json()["user_name"] == "test_user"
    assert response.json()["user_id"] == 1