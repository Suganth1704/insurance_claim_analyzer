from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):

    GROQ_API_KEY:str
    GL_GEN_AI_API_KEY:str

    #Dir
    BASE_DIR:str = os.path.dirname(os.path.abspath(__name__))
    DATA_DIR:str = os.path.join(BASE_DIR, "data")
    IMAGE_DIR:str = os.path.join(DATA_DIR, "images")
    
    #Models
    GOOGLE_GEM: str = "gemini-2.5-flash"
    GROQ_GPT: str = "openai/gpt-oss-120b"


    APP_NAME: str = "Insurance_claim_analyzer"

    class Config:
        BASE_DIR = os.getcwd()
        env_file = os.path.join(BASE_DIR, ".env")
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    """
    Cache settings to avoid reading .env file repeatedly.
    lru_cache ensures we only create one Settings instance.
    """
    return Settings()