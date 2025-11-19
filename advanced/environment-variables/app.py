import uvicorn
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Read environment variables
APP_NAME = os.getenv('APP_NAME', 'Default App')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS', '100'))
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/db')
API_KEY = os.getenv('API_KEY', None)

class Config(BaseModel):
    app_name: str
    version: str
    environment: str
    debug: bool
    max_connections: int
    database_url: str
    api_key_configured: bool

@app.get('/')
def read_root():
    return {
        "message": f"Welcome to {APP_NAME}",
        "version": APP_VERSION,
        "environment": ENVIRONMENT
    }

@app.get('/health')
def health_check():
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "debug": DEBUG
    }

@app.get('/config')
def get_config() -> Config:
    """Return current configuration (without sensitive values)"""
    return Config(
        app_name=APP_NAME,
        version=APP_VERSION,
        environment=ENVIRONMENT,
        debug=DEBUG,
        max_connections=MAX_CONNECTIONS,
        database_url=DATABASE_URL.replace(DATABASE_URL.split('@')[-1], '@***') if '@' in DATABASE_URL else DATABASE_URL,
        api_key_configured=API_KEY is not None
    )

@app.get('/env')
def show_env():
    """Show all environment variables (careful in production!)"""
    if not DEBUG:
        return {"error": "Only available in debug mode"}
    
    # Filter out sensitive variables
    safe_env = {
        k: v for k, v in os.environ.items() 
        if not any(sensitive in k.lower() for sensitive in ['password', 'secret', 'key', 'token'])
    }
    return {"environment_variables": safe_env}

if __name__ == '__main__':
    uvicorn.run(
        app, 
        host='0.0.0.0', 
        port=8000,
        log_level='debug' if DEBUG else 'info'
    )
