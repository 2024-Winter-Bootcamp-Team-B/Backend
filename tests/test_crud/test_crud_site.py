"""
테스트 해야할 것 
1. get_most_blocked_site
2. site_exist_check
3. add_site
"""

"""
#given
#when
#then
"""
from app.crud.site import add_site, get_most_blocked_site, site_exist_check


def test_add_site(db_session) :
    #given
    test_url = "example.com"
    #when
    test_site = add_site(db_session, test_url)
    #then
    assert test_url == test_site.url
    assert test_site.blocked_cnt == 1

def test_get_most_blocked_site(db_session):
    #given
    add_site(db_session, "example01.com")
    add_site(db_session, "example02.com")
    add_site(db_session, "example03.com")
    add_site(db_session, "example04.com")
    add_site(db_session, "example05.com")
    add_site(db_session, "example06.com")
    add_site(db_session, "example01.com")
    #when
    test_blocked_sites = get_most_blocked_site(db_session)
    top_url = []
    for url in test_blocked_sites :
        top_url.append(url)

    #then
    assert len(test_blocked_sites) == 5
    assert "example06.com" not in top_url 

def test_site_exist_check(db_session):
    #given
    test_site = add_site(db_session, "example.com")
    #when
    test_does_exist = site_exist_check(db_session, "example.com")
    test_does_not_exist = site_exist_check(db_session, "test.com")
    #then
    assert test_does_exist is not None
    assert test_does_not_exist is None