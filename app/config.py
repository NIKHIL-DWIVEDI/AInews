from dotenv import load_dotenv
import os
# sys.path.append("../")
class Config:
    """Configuration class for the application."""
    
    def __init__(self):
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env.development')
        load_dotenv(dotenv_path=env_path)
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.news_base_url = "https://newsapi.org/v2/top-headlines"
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.llm_provider = "groq"
        self.model = "llama-3.3-70b-versatile"
        self.temperature = 0.7
        self.llm_max_tokens = 1000



    def validate_news_api_key(self):
        if not self.news_api_key:
            raise EnvironmentVariableNotFoundError("NEWS_API_KEY not found in environment variables.")
        return self.news_api_key
    
    def validate_groq_api_key(self):
        if not self.groq_api_key:
            raise EnvironmentVariableNotFoundError("GROQ_API_KEY not found in environment variables.")
        return self.groq_api_key
    
class EnvironmentVariableNotFoundError(Exception):
    """Custom exception for missing environment variables."""
    pass

config = Config()
try:
    config.validate_news_api_key()
    print("NEWS_API_KEY is valid and loaded successfully.")
    config.validate_groq_api_key()
    print("GROQ_API_KEY is valid and loaded successfully.")
except EnvironmentVariableNotFoundError as e:
    print(f"Error: {e}")
    exit(1)
    