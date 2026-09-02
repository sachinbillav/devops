from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# connect_args is needed for SQLite multi-threading
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to yield a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()