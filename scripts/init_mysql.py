from sqlalchemy import text
from db.mysql import engine,Base
from db import models

def init():
    print("Creating tables(if not exist)...")

    Base.metadata.create_all(bind=engine)

    print("Pinging mysql...")
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("Mysql ok")

if __name__=="__main__":
    init()