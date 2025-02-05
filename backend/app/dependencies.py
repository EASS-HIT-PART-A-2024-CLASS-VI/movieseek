from app.database import SessionLocal

def get_db():
    """
    Dependency function to get a database session.
    Ensures session cleanup after request handling.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
