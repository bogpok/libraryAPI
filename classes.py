from pydantic import BaseModel # data validation library for Python

class Item(BaseModel):
    text: str # required (since there is no default value)
    is_done: bool = False