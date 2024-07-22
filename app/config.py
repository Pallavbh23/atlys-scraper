from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import Field
class Settings(BaseSettings):
    scraping_url: str = "https://dentalstall.com/shop/"
    static_token: str
    proxy: Optional[str] = Field(default=None)
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    redis_cache_timeout: int = 300  # Cache timeout in seconds (5 minutes)

    class Config:
        env_file = ".env"

settings = Settings()
