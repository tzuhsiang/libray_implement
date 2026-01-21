from mcp.server.fastmcp import FastMCP
from database import SessionLocal
import crud, schemas, models
from typing import Optional

# Initialize FastMCP
mcp = FastMCP("LibriFlow Manager")

@mcp.tool()
def add_book(title: str, author: str, status: str = "unread", rating: int = 0) -> str:
    """新增書籍 (status options: unread, reading, finished)"""
    db = SessionLocal()
    try:
        # Validate status if needed or let schemas do it (though schema validation happens inside Pydantic model init)
        book_in = schemas.BookCreate(
            title=title,
            author=author,
            status=status,
            rating=rating
        )
        book = crud.create_book(db, book_in)
        return f"Added book: {book.title} (ID: {book.id})"
    except Exception as e:
        return f"Error adding book: {str(e)}"
    finally:
        db.close()

@mcp.tool()
def list_books(limit: int = 20, offset: int = 0) -> str:
    """列出書籍清單"""
    db = SessionLocal()
    try:
        books = crud.get_books(db, skip=offset, limit=limit)
        if not books:
            return "No books found."
        
        # Format books as a simple list string
        book_list = []
        for b in books:
            book_list.append(f"ID: {b.id}, Title: {b.title}, Author: {b.author}, Rating: {b.rating}, Status: {b.status}")
        
        return "\n".join(book_list)
    except Exception as e:
        return f"Error listing books: {str(e)}"
    finally:
        db.close()

@mcp.tool()
def delete_book(book_id: int) -> str:
    """刪除書籍"""
    db = SessionLocal()
    try:
        success = crud.delete_book(db, book_id)
        if success:
            return f"Deleted book ID: {book_id}"
        else:
            return f"Book ID {book_id} not found"
    except Exception as e:
        return f"Error deleting book: {str(e)}"
    finally:
        db.close()

@mcp.tool()
def update_book_rating(book_id: int, rating: int) -> str:
    """修改書本評價 (0-5)"""
    db = SessionLocal()
    try:
        # Pydantic validation handles range check
        book_update = schemas.BookUpdate(rating=rating)
        book = crud.update_book(db, book_id=book_id, book_update=book_update)
        if book:
            return f"Updated book {book_id} rating to {rating}"
        else:
            return f"Book ID {book_id} not found"
    except Exception as e:
        return f"Error updating rating: {str(e)}"
    finally:
        db.close()

@mcp.tool()
def update_book_status(book_id: int, status: str) -> str:
    """修改閱讀狀態 (unread, reading, finished)"""
    db = SessionLocal()
    try:
        book_update = schemas.BookUpdate(status=status)
        book = crud.update_book(db, book_id=book_id, book_update=book_update)
        if book:
            return f"Updated book {book_id} status to {status}"
        else:
            return f"Book ID {book_id} not found"
    except Exception as e:
        return f"Error updating status: {str(e)}"
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run()
