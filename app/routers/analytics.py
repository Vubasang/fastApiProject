from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from easycharts import ChartServer

import pandas as pd
import matplotlib.pyplot as plt

import collections

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

from .models import Order

@router.get("/analytics", response_class=HTMLResponse)
def form_get(request: Request):
    SQLALCHEMY_DATABASE_URL = "postgresql://wubashang:wubashang_password@gogotech.ru:7777/db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    BaseException = declarative_base()
    db = SessionLocal()
    result = db.query(Order.date).all()
    results = sorted([a[0].strftime('%Y/%m/%d') for a in result])

    array_result = {}
    for a in results:
        try:
            array_result[a] += 1
        except KeyError:
            array_result[a] = 1

    for item in sorted(array_result):
        print(item, array_result[item])

    c = collections.Counter(array_result)
    values = []
    counts = []
    for value, key in c.items():
        values.append(value)
        counts.append(key)

    plt.figure(figsize=(14.9999, 7))
    plt.plot(values, counts)
    for a, b in zip(values, counts):
        plt.text(a, b, str(b))
    plt.title('Общее количество заказов (по дням)', fontsize=18, color='b')
    plt.xlabel('Дата', fontsize=14)
    plt.ylabel('Общее количество заказов', fontsize=14)
    plt.gcf().autofmt_xdate()
    plt.savefig('static/my_plot.png')

    return templates.TemplateResponse('analytics.html', context={'request': request, 'array_result': array_result, 'values': values, 'counts': counts})

