# build a schema using pydantic
from pydantic import BaseModel


class Order(BaseModel):
    id: int
    date: str

    class Config:
        orm_mode = True

