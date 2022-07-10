from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from easycharts import ChartServer
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

import collections

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

from .models import Order
from .models import Statusorder

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

    # Всего сколько заказов
    result_order = db.query(Order.date).all()
    result_orders = sorted([a[0].strftime('%Y/%m/%d') for a in result_order])

    array_result = {}
    for a in result_orders:
        try:
            array_result[a] += 1
        except KeyError:
            array_result[a] = 1

    # Количество тестовых заказов
    order_test = db.query(Order.id).filter((Order.unit_id == 1) | (Order.unit_id == 2) | (Order.unit_id == 3)).all()
    order_tests = sorted([a[0] for a in order_test])

    date_test = db.query(Order.date).filter((Order.unit_id == 1) | (Order.unit_id == 2) | (Order.unit_id == 3)).all()
    date_tests = sorted([a[0].strftime('%Y/%m/%d') for a in date_test])

    array_date = {}
    for a in date_tests:
        try:
            array_date[a] += 1
        except KeyError:
            array_date[a] = 1

    for i in array_result:
        if i not in array_date:
            array_date[i] = 0

    array_date_test = dict(sorted(array_date.items(), key=lambda x: datetime.strptime(x[0], "%Y/%m/%d")))

    # Количество удаленных заказов
    order_canceled = db.query(Statusorder.order_id).filter(Statusorder.status == 'CANCELED').all()
    order_canceleds = sorted([a[0] for a in order_canceled])

    list_order_canceleds = [i for i in order_canceleds if i not in order_tests]
    date_order_canceled = []
    for i in list_order_canceleds:
        date_order_canceled.append(db.query(Order.date).filter(Order.id == i).all())

    date_order_canceleds = sorted([a[0][0].strftime('%Y/%m/%d') for a in date_order_canceled])
    array_order_canceleds = {}

    for a in date_order_canceleds:
        try:
            array_order_canceleds[a] += 1
        except KeyError:
            array_order_canceleds[a] = 1

    for i in array_result:
        if i not in array_order_canceleds:
            array_order_canceleds[i] = 0

    array_canceleds = dict(sorted(array_order_canceleds.items(), key=lambda x: datetime.strptime(x[0], "%Y/%m/%d")))

    # Общее количество заказов по дням
    c_date = collections.Counter(array_result) - collections.Counter(array_date_test) - collections.Counter(array_canceleds)
    values = []
    counts = []
    for value, key in c_date.items():
        values.append(value)
        counts.append(key)

    plt.figure(figsize=(14.9, 7))
    plt.plot(values, counts)
    for a, b in zip(values, counts):
        plt.text(a, b, str(b))
    plt.title('Общее количество заказов (по дням)', fontsize=18, color='b')
    plt.xlabel('Дата', fontsize=14)
    plt.ylabel('Общее количество заказов', fontsize=14)
    plt.gcf().autofmt_xdate()
    plt.savefig('static/my_plot.png')

    array_total = {}
    for k, v in array_result.items():
        array_total[k] = v - array_date_test.get(k, 0) - array_canceleds.get(k, 0)



    return templates.TemplateResponse('analytics.html', context={'request': request, 'array_result': array_result, 'values': values,
                                                                 'counts': counts, 'order_tests': order_tests, 'date_tests': array_date_test,
                                                                 'order_canceled': list_order_canceleds,
                                                                 'date_order_canceleds': date_order_canceleds,
                                                                 'array_order_canceleds': array_canceleds, 'array_total': array_total})
