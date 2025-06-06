from datetime import datetime
from pydantic import BaseModel, Field, validator

class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    year: int
    author_id: int

    @validator('year')
    def year_not_future(cls, v):
        current_year = datetime.now().year
        if v > current_year:
            raise ValueError("Год издания не может быть в будущем")
        return v

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True