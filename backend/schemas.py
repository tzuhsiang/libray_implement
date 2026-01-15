from pydantic import BaseModel, Field, validator
from typing import Optional


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    status: Optional[str] = Field(default="unread")
    rating: Optional[int] = Field(default=0, ge=0, le=5)

    @validator("status")
    def validate_status(cls, v):
        allowed_statuses = ["unread", "reading", "finished"]
        if v not in allowed_statuses:
            raise ValueError(f"status must be one of {allowed_statuses}")
        return v


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = None
    rating: Optional[int] = Field(None, ge=0, le=5)

    @validator("status")
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ["unread", "reading", "finished"]
            if v not in allowed_statuses:
                raise ValueError(f"status must be one of {allowed_statuses}")
        return v


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True
