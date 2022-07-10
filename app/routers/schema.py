# build a schema using pydantic
from pydantic import BaseModel


class Order(BaseModel):
    id: int
    date: str
    unit_id: int

    class Config:
        orm_mode = True


class StatusOrder(BaseModel):
    id: int
    order_id: int
    status: str
    created: str

    class Config:
        orm_mode = True