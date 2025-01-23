import logging, pytest
from datetime import datetime
from app.crud.lock import *
from app.crud.site import add_site
from app.crud.user import add_user
from app.services.check_session_service import check_db as check
from tests.conftest import reset_database


@pytest.mark.order(1)
def test_set_locked_info(db_session):
        #초기화
    check(db_session, "test_set_locked_info")
    reset_database(db_session)

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
    check(db_session, "test_add_locked_info")
    #given 
    test_user_id = 1 #test01 
    test_site_id = 1 #example01.com
    #when
    test_locked = add_locked(db_session, test_user_id, test_site_id, datetime.now())
    #then
    assert test_locked is not None
    assert test_locked.user_id == test_user_id
    assert test_locked.site_id == test_site_id



@pytest.mark.order(3)
def test_add_block_site_version01(db_session):
    check(db_session, "test_add_block_site_version01")
    #given
    test_user_id = 1
    test_siteURL = ["example01.com", "example02.com"]
    test_goal_time = datetime.now()

    #when
    test_locked_sites = add_block_sites(
        db_session, test_user_id, test_siteURL, test_goal_time
    )
    assert test_locked_sites is not None
    assert len(test_locked_sites) == 2

@pytest.mark.order(4)
def test_add_block_site_version02(db_session):
    check(db_session, "test_add_block_site_version02")
    #given
    test_user_id = 2
    test_goal_time = datetime.now()
        # 이미 등록되어 있는 사이트와 등록되어 있지 않은 사이트를 차단하는 경우
    test_siteURL = ["example03.com", "example04.com"]
    #when
    test_locked_sites = add_block_sites(
        db_session, test_user_id, test_siteURL, test_goal_time
    )
    #then
    assert test_locked_sites is not None
    assert len(test_locked_sites) == 2


@pytest.mark.order(5)
def test_unblock_sites_by_user(db_session):
    check(db_session, "test_unblock_sites_by_user")
    #given
    test_user_id01 = 1
    #when
    unblock_sites_by_user(db_session, test_user_id01)
    #then
    test_sites = get_blocked_sites(db_session, test_user_id01)
    assert len(test_sites) == 0





def test_get_blocked_sites(db_session):
    reset_database(db_session)

    #given
    test_user_id01 = 1
    test_user_id02 = 2

    test_goal_time01 = datetime.now()
    test_goal_time02 = datetime.now()
    test_siteURL01 = ["example01.com", "example02.com"]
    test_siteURL02 = ["example03.com", "example04.com"]

    test_locked_sites01 = add_block_sites(
        db_session, test_user_id01, test_siteURL01, test_goal_time01
    )
    test_locked_sites02 = add_block_sites(
        db_session, test_user_id02, test_siteURL02, test_goal_time02
    )

    #when
    test_sites01 = get_blocked_sites(db_session, test_user_id01)
    test_sites02 = get_blocked_sites(db_session, test_user_id02)

    print("---------------------test_sites01's url =---------------------------")
    for s in test_sites01 :
        print(f"{s.url}")
    assert len(test_sites01) == 2
    assert len(test_sites02) == 2
    assert all(site.url in ["example03.com", "example04.com"]
                for site in test_sites02)
    assert all(site.url in ["example01.com", "example02.com"]
                for site in test_sites01)
