from pydantic import BaseModel # data validation library for Python
from typing import Optional

class Item(BaseModel):
    text: str # required (since there is no default value)
    is_done: bool = False

class Book(BaseModel):
    name: str
    author: str
    year: int
    is_available: bool

class UpdateBook(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    is_available: Optional[bool] = None