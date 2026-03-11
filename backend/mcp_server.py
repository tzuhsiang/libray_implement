import json
from typing import Optional
from fastmcp import FastMCP
from skills import (
    add_book_logic,
    list_books_logic,
    delete_book_logic,
    update_book_rating_logic,
    update_book_status_logic,
)

mcp = FastMCP("LibriFlow Manager")

def _wrap(results):
    """統一回傳格式：附上 total 讓 LLM 直接讀取精確筆數"""
    if isinstance(results, list):
        return json.dumps(
            {"total": len(results), "data": results},
            ensure_ascii=False,
            default=str,
        )
    return json.dumps(
        {"data": results},
        ensure_ascii=False,
        default=str,
    )

@mcp.tool()
def add_book(title: str, author: str, status: str = "unread", rating: int = 0) -> str:
    """新增書籍 (status options: unread, reading, finished)"""
    result = add_book_logic(title, author, status, rating)
    return _wrap(result)

@mcp.tool()
def list_books(limit: int = 20, offset: int = 0) -> str:
    """列出書籍清單"""
    results = list_books_logic(limit, offset)
    return _wrap(results)

@mcp.tool()
def delete_book(book_id: int) -> str:
    """刪除書籍"""
    success = delete_book_logic(book_id)
    return _wrap({"success": success, "book_id": book_id})

@mcp.tool()
def update_book_rating(book_id: int, rating: int) -> str:
    """修改書本評價 (0-5)"""
    result = update_book_rating_logic(book_id, rating)
    return _wrap(result if result else {"error": "Book not found"})

@mcp.tool()
def update_book_status(book_id: int, status: str) -> str:
    """修改閱讀狀態 (unread, reading, finished)"""
    result = update_book_status_logic(book_id, status)
    return _wrap(result if result else {"error": "Book not found"})

if __name__ == "__main__":
    # 以 streamable-http 模式啟動，使其可以被外部透過 HTTP 呼叫
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)
