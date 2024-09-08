from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "token"
    DB_HOST: str = "host"
    DB_PORT: int = 0000
    DB_NAME: str = "name"
    DB_PASS: str = "password"
    DB_USER: str = "admin"

    CACHE_HOST: str = "localhost"
    CACHE_PORT: int = 6378
    CACHE_DB: int = 0

settings = Settings()