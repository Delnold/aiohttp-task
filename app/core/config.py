import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Authentication(BaseSettings):
    jwt_secret_ket: str = str(os.environ.get("JWT_SECRET_KEY"))


auth_settings = Authentication()


class DbSettings(BaseSettings):
    db_host: str = str(os.environ.get("DB_HOST"))
    db_port: int = os.environ.get("DB_PORT")
    db_name: str = os.environ.get("DB_DATABASE")
    db_user: str = os.environ.get("DB_USERNAME")
    db_pass: str = os.environ.get("DB_PASSWORD")


db_settings = DbSettings()
