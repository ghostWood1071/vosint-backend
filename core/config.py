from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "V-OSINT API"
    APP_ORIGINS: List[str]

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 6082
    APP_STATIC_DIR: str = "static"

    PRIVATE_KEY: str
    PUBLIC_KEY: str

    # MONGO_DETAILS: str = (
    #     "mongodb://vosint:vosint_2022@118.70.52.237:27017/?authMechanism=DEFAULT"
    # )
    MONGO_DETAILS: str  # = "mongodb://localhost:27017"
    DATABASE_NAME: str  # = "vosint_db"

    mong_host: str  # = "localhost"  # "118.70.52.237"
    mongo_port: int  # = 27017
    mongo_username: str  # = "vosint"
    mongo_passwd: str  # = "vosint_2022"
    mongo_db_name: str  # = "vosint_db"

    ELASTIC_CONNECT: str  # = "http://localhost:9200"

    ROOT_PATH: str  # = ""

    SUMMARIZE_API: str  # = "http://sumthesis.aiacademy.edu.vn/ext"

    PIPELINE_API: str

    KEYWORD_EXTRACTION_API: str

    TRANSLATE_API: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        secrets_dir = "./secrets"
        case_sensitive = True


settings = Settings()
