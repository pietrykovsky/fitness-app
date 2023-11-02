import os


# common
PROJECT_NAME = "Fitness API"
API_STR = "/api"


# database related constants
DB_DRIVERNAME = "postgresql+psycopg2"
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")


# security
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://0.0.0.0:3000",
    "http://0.0.0.0:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]
