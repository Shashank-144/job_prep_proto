from sqlalchemy import Column,Integer, String,DateTime,func,Index

from db.mysql import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    email=Column(String(191),unique=True,index=True,nullable=False)
    password_hash=Column(String(255),nullable=False)
    created_at=Column(DateTime,server_default=func.now(),nullable=False)
    updated_at=Column(DateTime,onupdate=func.now())


