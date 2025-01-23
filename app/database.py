# 데이터베이스 연결 및 세션 관리
# SQLAlchemy 엔진과 세션 설정
# 구현한 api실험은 swagger사용하면 되니까 db연동은 나중에 해도 될 듯.
import os

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv

load_dotenv()

# 환경 변수 가져오기
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

# TESTING 환경 확인
if os.getenv("TESTING") == "TRUE":
    # SQLite 메모리 데이터베이스
    engine = create_engine( 
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )  
else:
    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(db_url)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# 데이터베이스 세션 제공
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
