from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import settings


class Base(DeclarativeBase):
    pass

engine=create_engine(
    settings.mysql_url,
    pool_size=settings.MYSQL_POOL_SIZE,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800,
    future=True,
)

SessionLocal=sessionmaker(bind=engine,autoflush=False, autocommit=False, future=True)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()