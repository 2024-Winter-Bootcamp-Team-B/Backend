from datetime import datetime
import logging

import pytest
from app.crud.lock import add_block_sites, add_locked, get_blocked_sites, unblock_sites_by_user
from app.crud.site import add_site
from app.crud.user import add_user

from app.models import Base
from conftest import reset_database
"""
테스트 해야할 것 
1. get_blocked_sites
2. unblock_sites_by_user
3. add_block_sites
4. add_locked
"""

"""
#given
#when
#then
"""

@pytest.mark.order(1)
def test_set_locked_info(db_session):
        #초기화
    reset_database(db_session, Base.metadata)

        #유저 등록하기
    add_user(db_session, "test01", "test01", "test_user01", "example1@naver.com")
    add_user(db_session, "test02", "test02", "test_user02", "example2@naver.com")
        #사이트 차단
    add_site(db_session, "example01.com")
    add_site(db_session, "example02.com")
    add_site(db_session, "example03.com")
    pass



@pytest.mark.order(2)
def test_add_locked(db_session):
    #given
    test_user_id = 1
    test_site_id = 1
    #when
    test_locked = add_locked(db_session, test_user_id, test_site_id, datetime.now())
    #then
    assert test_locked is not None
    assert test_locked.user_id == test_user_id
    assert test_locked.site_id == test_site_id

    pass



@pytest.mark.order(3)
def test_add_block_site_version01(db_session):
    #given
    test_user_id = 1
    test_siteURL = ["example01.com", "example02.com"]
    test_goal_time = datetime.now()

    #when
    add_block_sites(
        db_session, test_user_id, test_siteURL, test_goal_time
    )
@pytest.mark.order(4)
def test_add_block_site_version02(db_session):
    #given
    test_user_id = 2
    test_goal_time = datetime.now()
        # 이미 등록되어 있는 사이트와 등록되어 있지 않은 사이트를 차단하는 경우
    test_siteURL = ["example03.com", "example04.com"]
    #when
    add_block_sites(
        db_session, test_user_id, test_siteURL, test_goal_time
    )
    #then

@pytest.mark.order(5)
def test_get_blocked_sites(db_session, caplog):
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)

    #given
    test_user_id01 = 1
    test_user_id02 = 2

    #when
    test_sites01 = get_blocked_sites(db_session, test_user_id01)
    test_sites02 = get_blocked_sites(db_session, test_user_id02)


    # then
    with caplog.at_level(logging.INFO):
        for site in test_sites01:
            logger.info(f"Blocked site for user 1: {site.url}")
        for site in test_sites02:
            logger.info(f"Blocked site for user 2: {site.url}")
    # 로그 출력 확인 
    for record in caplog.records:
        print(record.message)  # 기록된 메시지를 출력
    
    assert len(test_sites01) == 2
    assert len(test_sites02) == 2
    assert all(site.url in ["example03.com", "example04.com"]
                for site in test_sites02)
    assert all(site.url in ["example01.com", "example02.com"]
                for site in test_sites01)

    

# @pytest.mark.order(6)
# def test_unblock_sites_by_user(db_session):
#     #given
#     test_user_id01 = 1
#     #when
#     unblock_sites_by_user(db_session, test_user_id01)
#     #then
#     test_sites = get_blocked_sites(db_session, test_user_id01)
#     assert len(test_sites) == 0