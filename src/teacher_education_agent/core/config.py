"""Environment-backed application settings."""
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str = "postgresql+asyncpg://teacher_agent:change-me@localhost:5432/teacher_agent"
    langgraph_checkpoint_url: str = "postgresql://teacher_agent:change-me@localhost:5432/teacher_agent"
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"
    dashscope_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    dashscope_api_key: str = ""
    qwen_model: str = "qwen-plus"
    embedding_model: str = "text-embedding-v4"
    vector_dimension: int = Field(1024, ge=1)
    vector_index: str = "hnsw"
    funasr_base_url: str = "http://localhost:8001"
    funasr_model: str = "iic/SenseVoiceSmall"
    model_timeout_seconds: float = Field(30, gt=0)
    model_max_retries: int = Field(2, ge=0, le=5)

@lru_cache
def get_settings() -> Settings:
    return Settings()
