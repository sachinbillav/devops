import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Read data directory from environment variable, fallback to "/data" (or "." for local development)
DATA_DIR = os.getenv("DATA_DIR", "/data")

# 2. Ensure the directory exists inside the container
os.makedirs(DATA_DIR, exist_ok=True)

# 3. Form the full SQLite path: /data/app.db
DB_FILE_PATH = os.path.join(DATA_DIR, "app.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()