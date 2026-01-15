from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    """取得所有書籍清單"""
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    """根據 ID 取得單一書籍"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    """新增書籍"""
    db_book = models.Book(
        title=book.title,
        author=book.author,
        status=book.status,
        rating=book.rating
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate) -> Optional[models.Book]:
    """更新書籍資訊"""
    db_book = get_book(db, book_id)
    if db_book is None:
        return None
    
    # 只更新有提供的欄位
    update_data = book_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    """刪除書籍"""
    db_book = get_book(db, book_id)
    if db_book is None:
        return False
    
    db.delete(db_book)
    db.commit()
    return True
