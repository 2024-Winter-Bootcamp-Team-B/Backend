'''
- 데이터 구조 정의
- requrest, response에 사용되는 데이터 모델 정의
'''

from pydantic import BaseModel
from typing import List

class Site(BaseModel):
    site_id: int
    url: str
    blocked_cnt: int

    class Config:
        orm_mode = True # orm_mode를 활성화하면 Pydantic이 ORM 객체를 자동으로 읽어들여 스키마에 맞는 JSON 응답을 생성할 수 있음.

class BlockedSitesResponse(BaseModel):
    user_id: int
    blocked_sites: List[Site]

# EX>

# from pydantic import BaseModel
# import datetime


# class UserBase(BaseModel):
#     nickname: str


# class UserCreate(UserBase):
#     pass


# class UserModify(UserBase):
#     pass


# class UserResponse(UserBase):
#     id: int
#     created_at: datetime.datetime
#     updated_at: datetime.datetime


# class ChatroomCreate(BaseModel):
#     user_id: int
#     mentor_id: int


# class ChatroomResponse(BaseModel):
#     id: int
#     user_id: int
#     mentor_id: int
#     created_at: datetime.datetime
#     updated_at: datetime.datetime


# class MentorBase(BaseModel):
#     name: str
#     description: str


# class MentorCreate(MentorBase):
#     pass


# class MentorResponse(MentorBase):
#     id: int
#     created_at: datetime.datetime
#     updated_at: datetime.datetime


# class PrescriptionResponse(BaseModel):
#     id: int
#     user_id: int
#     mentor_id: int
#     content: str
#     created_at: datetime.datetime
#     updated_at: datetime.datetime


# class PrescriptionCreate(BaseModel):
#     user_id: int
#     mentor_id: int
#     content: str