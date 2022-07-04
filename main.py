from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Order

from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def main():
    SQLALCHEMY_DATABASE_URL = "postgresql://wubashang:wubashang_password@gogotech.ru:7777/db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    BaseException = declarative_base()
    db = SessionLocal()
    result = db.query(Order).all()
    print(result)

    @app.get("/index/", response_class=HTMLResponse)
    async def orderlist(request: Request, hx_request: Optional[str] = Header(None)):
        context = {"request": request, 'result': result}
        if hx_request:
            return templates.TemplateResponse("partials/table.html", context)
        return templates.TemplateResponse("index.html", context)

if __name__ == '__main__':
    main()