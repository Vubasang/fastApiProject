from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime

from typing import Union

from .models import Order

from dotenv import load_dotenv
load_dotenv()

templates = Jinja2Templates(directory="templates")

router = APIRouter()


'''@router.get("/couriersalaries", response_class=HTMLResponse)
async def database_home(request: Request):
    key = os.getenv("database_key")
    print(key)
    return templates.TemplateResponse("couriersalaries.html", {"request": request})'''

@router.get("/couriersalaries", response_class=HTMLResponse)
def couriersalaries(request: Request):
    SQLALCHEMY_DATABASE_URL = "postgresql://wubashang:wubashang_password@gogotech.ru:7777/db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    BaseException = declarative_base()
    db = SessionLocal()
    # print('QUERY', db.query(Order.date))

    resultt = ''
    return templates.TemplateResponse('couriersalaries.html', context={'request': request, 'resultt': resultt})

@router.post('/couriersalaries', response_class=HTMLResponse)
def couriersalaries(request: Request, dateSelected: Union[str, None] = Form(None)):
    SQLALCHEMY_DATABASE_URL = "postgresql://wubashang:wubashang_password@gogotech.ru:7777/db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    BaseException = declarative_base()
    db = SessionLocal()
    # print('QUERY', db.query(Order.date))

    print(dateSelected)
    if(dateSelected):
        resultt = 'Зарплата у каждого курьера на ' + dateSelected + ' составляет:'
    else:
        resultt = "Пожалуйста выберите правильную дату"
    return templates.TemplateResponse('couriersalaries.html', context={'request': request, 'dateSelected': dateSelected, 'resultt': resultt})
