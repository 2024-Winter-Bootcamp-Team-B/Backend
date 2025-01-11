'''
- 데이터 구조 정의
- requrest, response에 사용되는 데이터 모델 정의
'''
# EX>

from pydantic import BaseModel
import datetime


class UserBase(BaseModel):
    nickname: str


class UserCreate(UserBase):
    pass


class UserModify(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


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