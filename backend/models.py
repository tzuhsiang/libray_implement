from sqlalchemy import Column, Integer, String
from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    status = Column(String, default="unread")  # unread, reading, finished
    rating = Column(Integer, default=0)  # 1-5, 0 表示未評分
