import os
from sqlalchemy import MetaData, StaticPool, create_engine
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
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )  
else:
    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(db_url)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 기본 모델 클래스
Base = declarative_base()

# 데이터베이스 세션 제공
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clear_db():
    meta = MetaData()
    meta.reflect(bind=engine)
    with engine.connect() as conn:
        for table in reversed(meta.sorted_tables):
            conn.execute(table.delete())
        conn.commit()