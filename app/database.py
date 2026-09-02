import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Fetch the database URL from environment variable
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Hard-fail immediately if DATABASE_URL is not set
if not SQLALCHEMY_DATABASE_URL:
    print("\n[FATAL ERROR] DATABASE_URL environment variable is not set!", file=sys.stderr)
    print("Cannot proceed without an active database configuration.\n", file=sys.stderr)
    raise RuntimeError("DATABASE_URL environment variable is required.")

# 3. Prevent silent fallback to SQLite if you only want RDS/PostgreSQL
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    print("\n[WARNING] Using SQLite database instead of PostgreSQL/RDS.\n", file=sys.stderr)
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,  # Automatically tests connection health before executing queries
        pool_size=5,
        max_overflow=10
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()