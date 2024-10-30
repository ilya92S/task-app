from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DB_HOST: str = "host"
    DB_PORT: int = 0000
    DB_NAME: str = "name"
    DB_PASS: str = "password"
    DB_USER: str = "admin"
    DB_DRIVER: str = "postgresql+asynсpg"

    CACHE_HOST: str = "host"
    CACHE_PORT: int = 000
    CACHE_DB: int = 0

    SECRET_KEY: str = "key"
    ALGORITHM: str = "algo"

    GOOGLE_SECRET_KEY: str = ""
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    YANDEX_SECRET_KEY: str = ""
    YANDEX_CLIENT_ID: str = ""
    YANDEX_REDIRECT_URI: str = ""
    YANDEX_TOKEN_URL: str = 'http://oauth.yandex.ru/token'

    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def yandex_redirect_url(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri={self.YANDEX_REDIRECT_URI}"

    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
