from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.env import DATABASE_URL

# Create a new SQLAlchemy engine instance
engine = create_engine(DATABASE_URL)
print("Connecting to database...")

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test
def test_db():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("Database connection is working.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        db.close()


# Run the test. if the script is executed directly
if __name__ == "__main__":
    test_db()
