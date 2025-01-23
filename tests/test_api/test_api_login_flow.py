from fastapi.testclient import TestClient
import pytest

from app.main import app


client = TestClient(app)

@pytest.mark.order(1)
def test_user_sign_up():
    #given
    test_login_id = "test"
    test_login_password = "test"
    test_user_name = "test_user"
    test_user_email = "test@example.com"

    #when
    response_sign_up = client.post(
        "/user/sign-up", 
        json={
            "login_id" : test_login_id,
            "login_password" : test_login_password,
            "name" : test_user_name, 
            "email" : test_user_email
        }
    )
    print()
    print(f" **** Response [sign up] =   {response_sign_up}")
    print(f" **** Response.json  [sign up] =   {response_sign_up.json()}")

    response_login = client.post(
        "/user/login-g", 
        json={
            "login_id" : test_login_id,
            "login_password" : test_login_password
        }
    )
    print()
    print(f" **** Response  [login] =   {response_login}")
    print(f" **** Response.json  [login] =   {response_login.json()}")


    response_not_login = client.post(
        "/user/login-g", 
        json={
            "login_id" : "notTest",
            "login_password" : "notTest"
        }
    )
    print()
    print(f" **** Response  [not_login] =   {response_not_login}")
    print(f" **** Response.json  [not_login] =   {response_not_login.json()}")
    #then 
    assert response_sign_up.status_code == 200
    assert response_login.status_code == 200
    assert response_not_login.status_code == 200
    assert response_sign_up.json().get("message") == "성공"
    assert response_login.json().get("message") == "성공"
    assert response_not_login.json().get("detail") == "아이디 혹은 비밀번호 오류"