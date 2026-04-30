from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.model.user import User
from app.core.security import getPasswordHash

def init_db():
    Base.metadata.create_all(bind=engine)
    create_root_admin()

def create_root_admin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.Username == "root").first()
        if existing:
            return
        
        root_admin = User(
            Username="root",
            HashedPassword=getPasswordHash("root"),
            UserRole="admin"
        )
        db.add(root_admin)
        db.commit()
        print("Created root admin user (username: root, password: root)")
    except Exception as e:
        print(f"Could not create root admin: {e}")
        db.rollback()
    finally:
        db.close()