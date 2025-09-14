from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db.models import User
from schemas.user import UserCreate

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(plain:str)->str:
    return pwd_context.hash(plain)

def verify_password(plain:str,hashed:str)->bool:
    return pwd_context.verify(plain,hashed)

def get_user_by_email(db:Session,email:str)-> User|None:
    return db.query(User).filter(User.email==email).first()

def create_user(db:Session,payload:UserCreate)->User:
    if get_user_by_email(db,payload.email):
        raise ValueError("Email already registered.")
    
    user=User(
        name=payload.name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

