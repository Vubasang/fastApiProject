import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Order as SchemaOrder

from schema import Order

from models import Order as ModelOrder

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
POSTGRES_USER: str = os.getenv("wubashang")
POSTGRES_PASSWORD = os.getenv("wubashang_password")
POSTGRES_SERVER: str = os.getenv("kjj", "localhost")
POSTGRES_PORT: str = os.getenv("7777", 5432) # default postgres port is 5432
POSTGRES_DB: str = os.getenv("db", "tdd")
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)
# app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post('/orders_order/', response_model=SchemaOrder)
async def order(orders_order: SchemaOrder):
    db_order = ModelOrder(title=order.id, rating=order.date)
    db.session.add(db_order)
    db.session.commit()
    return db_order


@app.get('/orders_order/')
async def order():
    orders_order = db.session.query(ModelOrder).all()
    return order


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)