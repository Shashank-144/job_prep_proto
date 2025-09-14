import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings:
    MYSQL_HOST:str =os.getenv("MYSQL_HOST","localhost")
    MYSQL_PORT:int = int(os.getenv("MYSQL_PORT","3306"))
    MYSQL_USER:str =os.getenv("MYSQL_USER","root")
    MYSQL_PASSWORD:str=os.getenv("MYSQL_PASSWORD","")
    MYSQL_DB:str=os.getenv("MYSQL_DB","resume_app")
    MYSQL_POOL_SIZE: int = int(os.getenv("MYSQL_POOL_SIZE", "10"))

    MONGO_URI:str ="mongodb"

    @property
    def mysql_url(self)->str:
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
            f"?charset=utf8mb4"

        )
    

def get_settings()->Settings:
    return Settings()

settings=get_settings()