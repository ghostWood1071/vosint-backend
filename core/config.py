from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "V-OSINT API"
    APP_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:5173",
        "http://127.0.0.1:2000",
        "http://118.70.48.144:2000",
        "http://192.168.1.101:2000",
        "http://118.70.52.237:2000",
    ]

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 6082
    APP_STATIC_DIR: str = "static"

    PRIVATE_KEY: str
    PUBLIC_KEY: str

    MONGO_DETAILS: str = "mongodb://127.0.0.1:27017"
    DATABASE_NAME: str = "vosint_db"

    mong_host = 'vosint_mongo'
    mongo_port = 27017
    mongo_username = "vosint"
    mongo_passwd = "vosint_2022"
    mongo_db_name = "vosint_db"

    ELASTIC_CONNECT: str = "http://elastic1:9200"

    ROOT_PATH: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        secrets_dir = "./secrets"
        case_sensitive = True


settings = Settings()
