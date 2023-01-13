from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "DEV"
    APP_PORT: int = 8000
    APP_HOST: str = "127.0.0.1"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str  # required
    DB_USER: str  # required
    DB_PASSWORD: str  # required
    DB_POOL_SIZE: int = 1
    SECRET_KEY: str  # required

    class Config:
        env_file = ".env"


settings = Settings()
