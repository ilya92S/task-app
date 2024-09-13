from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "token"
    DB_HOST: str = "host"
    DB_PORT: int = 0000
    DB_NAME: str = "name"
    DB_PASS: str = "password"
    DB_USER: str = "admin"
    DB_DRIVER: str = "postgresql+psycopg2"

    CACHE_HOST: str = "host"
    CACHE_PORT: int = 000
    CACHE_DB: int = 0

    SECRET_KEY: str = "key"
    ALGORITHM: str = "algo"

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

