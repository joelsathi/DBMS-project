from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "DEV"
    APP_PORT: int = 8000
    APP_HOST: str = "127.0.0.1"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str ="dbms_project"
    DB_USER: str = "Group26"
    DB_PASSWORD: str = "Abc@12345"
    DB_POOL_SIZE: int = 7

    class Config:
        env_file = ".env"


settings = Settings()
