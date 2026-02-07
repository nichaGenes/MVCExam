from sqlmodel import SQLModel, Session, create_engine
import os

DATABASE_URL = "postgresql://promise_user:promise_pass@127.0.0.1:5432/promise_tracker"

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    """Dependency สำหรับ inject database session เข้า route"""
    with Session(engine) as session:
        yield session



def create_db_and_tables():
    """สร้างตารางทั้งหมดจาก SQLModel metadata (ใช้ตอน dev เท่านั้น)"""
    # Import models here to ensure they are registered with SQLModel.metadata
    import models
    SQLModel.metadata.create_all(engine)



create_db_and_tables()