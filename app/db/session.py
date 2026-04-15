from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import time

DATABASE_URL = "mysql+pymysql://root:root@localhost/NYPD"

MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds

for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)

        with engine.connect() as conn:
            print("Database connection successful!")
        break
    except Exception as e:
        print(f"Database connection failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
        if attempt == MAX_RETRIES - 1:
            raise
        time.sleep(RETRY_DELAY)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()