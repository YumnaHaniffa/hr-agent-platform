#.env loading with Pydantic Settings
#Validate data types before the app runs
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Requirements: Validation and structured config
    openai_api_key: str
    database_url: str = "data/hr_platform.db"
    log_level: str = "INFO"
    port: int = 8000
    
    # This tells Pydantic to look for a file named .env
    model_config = SettingsConfigDict(env_file=".env")

# Create a single instance to use across the app
settings = Settings()
