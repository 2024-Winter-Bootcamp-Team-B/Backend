'''
- 데이터 구조 정의
- requrest, response에 사용되는 데이터 모델 정의
'''
# EX>

from pydantic import BaseModel
from datetime import datetime 

'''
class User_test(Base):
    __tablename__ = "user_test"
    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(KST),
        onupdate=lambda: datetime.now(KST),
    )
    is_deleted = Column(Boolean, nullable=False, default=False)

    prescriptions = relationship("Prescription", back_populates="user_test")
    chatrooms = relationship("Chatroom", back_populates="user_test")

'''
#사용자 모델의 기본 클래스 -> 얘를 상속받아서 데이터 스키마 생성
class UserBase(BaseModel):
    nickname: str

#새로운 사용자를 생성하는 API 요청에 사용 -> 생성할 때 검증
class UserCreate(UserBase):
    pass

#기존 사용자를 수정하는 API 요청에 사용 -> 수정할 때 검증
class UserModify(UserBase):
    pass

#API 응답에 사용 -> 그러면 UserResponse를 통해서 response를 하면 이 3개만 반환이 되는건가? ㅇㅇ +) userBASE를 상속 받았기 때문에 nickname도 포함
'''
ex 
{
    "id": 1,
    "nickname": "test_user",
    "created_at": "2025-01-13T12:34:56",
    "updated_at": "2025-01-13T12:34:56"
}
'''
class UserResponse(UserBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


# ---------------------------user table (진) ------------------------
'''
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
    updated_at = Column(DateTime, nullable=True)
    email = Column(String(30), nullable=False)

'''
class UserBase(BaseModel):
    email : str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id : int

# ---------------------------lock table (진) ------------------------ 이건 서버에서 관리하고 클라이언트와 연결되어 있지 않으니까 안해도 됨
'''
class Lock(Base):
    __tablename__ = "lock"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_deleted = Column(Boolean, nullable=True, default=False)
    goal_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: DateTime.now(KST))
    site_id = Column(Integer, ForeignKey("site.id"), nullable=False)
'''
# ---------------------------site table (진) ------------------------ 애도 굳이?
'''
class Site(Base):
    __tablename__ = "site"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    url = Column(String(300), nullable=False)
    blocked_cnt = Column(Integer, nullable=True, default=0)
'''
class SiteBase(BaseModel):
    url : str

class SiteCreate(SiteBase):
    pass

class SiteUpdate(SiteBase):
    pass

class SiteResponse(SiteBase):
    blocked_cnt : int

# ---------------------------history table (진) ------------------------ 
'''
class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    goal_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)

    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: DateTime.now(KST))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
'''
class HistoryBase(BaseModel):
    user_id : int

class HistoryCreate(HistoryBase):
    pass

class HistoryUpdate(HistoryBase):
    pass

class HistoryResponse(HistoryBase):
    start_time : datetime.datetime
    goal_time : datetime.datetime
    end_time : datetime.datetime
    created_at : datetime.datetime
    



class ChatroomCreate(BaseModel):
    user_id: int
    mentor_id: int


class ChatroomResponse(BaseModel):
    id: int
    user_id: int
    mentor_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class MentorBase(BaseModel):
    name: str
    description: str


class MentorCreate(MentorBase):
    pass


class MentorResponse(MentorBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PrescriptionResponse(BaseModel):
    id: int
    user_id: int
    mentor_id: int
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PrescriptionCreate(BaseModel):
    user_id: int
    mentor_id: int
    content: str