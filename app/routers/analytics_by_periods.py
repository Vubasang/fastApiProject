from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime

import json

from typing import Union

import plotly.express as px

import numpy as np
import matplotlib.pyplot as plt
import random

import collections

from .models import Couriers
from .models import Order
from .models import Statusorder
from .models import Organisations

from dotenv import load_dotenv
load_dotenv()

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/analytics_by_periods", response_class=HTMLResponse)
def analytics_by_periods(request: Request):
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
    return templates.TemplateResponse('analytics_by_periods.html', context={'request': request, 'resultt': resultt})

@router.post('/analytics_by_periods', response_class=HTMLResponse)
def analytics_by_periods(request: Request):
    SQLALCHEMY_DATABASE_URL = "postgresql://wubashang:wubashang_password@gogotech.ru:7777/db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    BaseException = declarative_base()
    db = SessionLocal()
    # print('QUERY', db.query(Order.date))

    return templates.TemplateResponse('analytics_by_periods.html', context={'request': request}
    )
