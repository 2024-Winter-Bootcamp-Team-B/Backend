import pytest, os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.database import Base, get_db, engine as default_engine
from app.main import app


# database.py에서 설정된 데이터파일 가져오기 
TEST_ENGINE = default_engine  

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)

# 테스트용 데이터베이스 초기화
@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    """테스트용 데이터베이스 초기화"""
    try:
        print("Preparing database...")
        Base.metadata.create_all(bind=TEST_ENGINE)
    except Exception as e:
        print(f"Error creating tables: {e}")
    yield
    print("Cleaning up database...")
    Base.metadata.drop_all(bind=TEST_ENGINE)

@pytest.fixture(scope="function")
def db_session():
    """각 테스트에서 사용할 세션"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



@pytest.fixture(scope="session")
def client(db_session):
    """FastAPI 클라이언트와 DB 의존성 오버라이드 설정"""
    def override_get_db():
        yield db_session  # 테스트 세션을 사용

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def set_testing_env():
    os.environ["TESTING"] = "TRUE"


def reset_database(session: Session):
    """데이터베이스를 초기화하는 함수."""
    print("Resetting database...")
    # 기존 테이블 삭제
    Base.metadata.drop_all(bind=TEST_ENGINE)
    # 새 테이블 생성
    Base.metadata.create_all(bind=TEST_ENGINE)
    print("Database reset complete.")