# build a schema using pydantic
from pydantic import BaseModel


class Order(BaseModel):
    id: int
    date: str

    class Config:
        orm_mode = True


class StatusOrder(BaseModel):
    id: int
    status: str
    created: str

    class Config:
        orm_mode = True