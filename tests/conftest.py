import pytest, os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db, engine as default_engine
from app.main import app


# 테스트용 엔진과 세션 설정
if os.getenv("TESTING") == "TRUE":
    TEST_ENGINE = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
else:
    TEST_ENGINE = default_engine  # 실제 데이터베이스 설정 사용

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


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI 클라이언트와 DB 의존성 오버라이드 설정"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def set_testing_env():
    os.environ["TESTING"] = "TRUE"