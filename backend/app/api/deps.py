from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

def get_db() -> Generator:
    """
    データベースセッションの依存関係
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
