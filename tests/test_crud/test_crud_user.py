from tests.conftest import reset_database
from app.crud.user import *
from app.database import Base
"""
테스트 해야할 것 
1. get_user_by_email
2. add_user
3. get_user_by_id
"""

"""
#given
#when
#then
"""

def test_user_all(db_session):
    reset_database(db_session,Base.metadata)
    #given
    test_login_id = "test01"
    test_login_password = "test01"
    test_email = "example@naver.com"
    test_user_name = "test_name"
    #when

        #add_user Test
    test_user = add_user(db_session,test_login_id, test_login_password, test_user_name, test_email)
        #get_user_by_id
    test_get_by_id = get_user_by_id(db_session, test_user.id)
    test_not_user = get_user_by_id(db_session, 2)
        #get_user_by_email
    test_get_by_email = get_user_by_email(db_session, test_user.email)

    #then
    assert test_user is not None
    assert test_not_user is None
    assert test_user is test_get_by_id
    assert test_get_by_id is test_get_by_email
