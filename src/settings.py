from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    environment: str = "production"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

settings = Settings()