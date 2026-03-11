from database import SessionLocal
import crud, schemas

def add_book_logic(title: str, author: str, status: str = "unread", rating: int = 0):
    """新增書籍邏輯"""
    db = SessionLocal()
    try:
        book_in = schemas.BookCreate(
            title=title,
            author=author,
            status=status,
            rating=rating
        )
        book = crud.create_book(db, book_in)
        return {"id": book.id, "title": book.title, "author": book.author, "status": book.status, "rating": book.rating}
    finally:
        db.close()

def list_books_logic(limit: int = 20, offset: int = 0):
    """列出書籍清單邏輯"""
    db = SessionLocal()
    try:
        books = crud.get_books(db, skip=offset, limit=limit)
        return [{"id": b.id, "title": b.title, "author": b.author, "rating": b.rating, "status": b.status} for b in books]
    finally:
        db.close()

def delete_book_logic(book_id: int):
    """刪除書籍邏輯"""
    db = SessionLocal()
    try:
        success = crud.delete_book(db, book_id)
        return success
    finally:
        db.close()

def update_book_rating_logic(book_id: int, rating: int):
    """修改書本評價邏輯"""
    db = SessionLocal()
    try:
        book_update = schemas.BookUpdate(rating=rating)
        book = crud.update_book(db, book_id=book_id, book_update=book_update)
        if book:
            return {"id": book.id, "rating": book.rating}
        return None
    finally:
        db.close()

def update_book_status_logic(book_id: int, status: str):
    """修改閱讀狀態邏輯"""
    db = SessionLocal()
    try:
        book_update = schemas.BookUpdate(status=status)
        book = crud.update_book(db, book_id=book_id, book_update=book_update)
        if book:
            return {"id": book.id, "status": book.status}
        return None
    finally:
        db.close()
