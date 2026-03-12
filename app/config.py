import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./osint.db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Keys (external services)
    SHODAN_KEY: str = os.getenv("SHODAN_KEY", "")
    CENSYS_ID: str = os.getenv("CENSYS_ID", "")
    CENSYS_SECRET: str = os.getenv("CENSYS_SECRET", "")
    VIRUSTOTAL_KEY: str = os.getenv("VIRUSTOTAL_KEY", "")
    HUNTER_IO_KEY: str = os.getenv("HUNTER_IO_KEY", "")
    
    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379")
    
    class Config:
        env_file = ".env"

settings = Settings()
