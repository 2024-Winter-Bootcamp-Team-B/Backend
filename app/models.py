'''
- 데이터베이스 테이블 구조 정의
- SQLAlchemy모델 정의. 데이터베이스의 테이블 스키마 표현
'''
#EX>

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.database import Base
import pytz

KST = pytz.timezone("Asia/Seoul")

# -----------------------------------------------------
class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    goal_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    login_id = Column(String(30), nullable=False)
    login_password = Column(String(30), nullable=False)
    user_name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
    updated_at = Column(DateTime, nullable=True)

class Locked(Base):
    __tablename__ = "Locked"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_deleted = Column(Boolean, nullable=True, default=False)
    goal_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
    site_id = Column(Integer, ForeignKey("site.id"), nullable=False)

class Site(Base):
    __tablename__ = "site"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    url = Column(String(300), nullable=False)
    blocked_cnt = Column(Integer, nullable=True, default=0)