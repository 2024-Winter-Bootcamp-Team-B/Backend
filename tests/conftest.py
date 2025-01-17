import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.models import Base
# 메모리 내 SQLite 데이터베이스 URL
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def db_engine():
    """테스트용 데이터베이스 엔진 생성"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine, request):
    """특정 파일에서는 데이터베이스 초기화를 하지 않음"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()

    # 특정 파일에서 초기화 생략
    if "no_reset" not in request.node.nodeid:
        reset_database(session, Base.metadata)

    try:
        yield session
    finally:
        session.close()


def reset_database(session, metadata):
    """
    데이터베이스를 초기화하는 함수.
    :param session: 현재 세션 객체
    :param metadata: 데이터베이스 메타데이터 객체
    """
    for table in reversed(metadata.sorted_tables):
        session.execute(table.delete())  # 테이블 데이터 삭제
    session.commit()