from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from easycharts import ChartServer
from datetime import datetime
import plotly.express as px

import numpy as np
import matplotlib.pyplot as plt
import random

import collections

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

from .models import Order
from .models import Statusorder
from .models import Organisations

import matplotlib
matplotlib.use("agg")

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

    id_order = db.query(Order.id).all()
    id_orders = sorted([a[0] for a in id_order])

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

    fig1 = plt.figure(figsize=(14.9, 7))
    plt.plot(values, counts)
    for a, b in zip(values, counts):
        plt.text(a, b, str(b))
    plt.title('Общее количество заказов (по дням)', fontsize=18, color='b')
    plt.xlabel('Дата', fontsize=14)
    plt.ylabel('Общее количество заказов', fontsize=14)
    plt.gcf().autofmt_xdate()
    fig1.savefig('static/Analytics_Total_number_of_orders.png')
    plt.close()

    array_total = {}
    for k, v in array_result.items():
        array_total[k] = v - array_date_test.get(k, 0) - array_canceleds.get(k, 0)

    # Количество заказов (по заведениям)
    for i in order_tests:
        id_orders.remove(i)
    for i in list_order_canceleds:
        id_orders.remove(i)

    date_order = []
    for i in id_orders:
        date_order.append(db.query(Order.date).filter(Order.id == i).all())
    date_orders = sorted([a[0][0].strftime('%Y/%m/%d') for a in date_order])

    unit_id_organisation = []
    for i in id_orders:
        unit_id_organisation.append(db.query(Order.unit_id).filter(Order.id == i).all())
    unit_id_organisations = [a[0][0] for a in unit_id_organisation]

    name_organisation = []
    for i in unit_id_organisations:
        name_organisation.append(db.query(Organisations.name).filter(Organisations.id == i).all())
    name_organisations = [a[0][0] for a in name_organisation]

    dict_date_and_organisation = list(zip(date_orders, name_organisations))
    dict_date_and_organisations = {}
    for a in dict_date_and_organisation:
        try:
            dict_date_and_organisations[a] += 1
        except KeyError:
            dict_date_and_organisations[a] = 1

    date_and_organisations = []
    number_of_orders_by_organization = []
    for value, key in dict_date_and_organisations.items():
        date_and_organisations.append(value)
        number_of_orders_by_organization.append(key)

    dates = []
    for i in range(len(date_and_organisations) - 1):
        if date_and_organisations[i][0] not in dates:
            dates.append(date_and_organisations[i][0])

    organisations = []
    for i in range(len(date_and_organisations) - 1):
        if date_and_organisations[i][1] not in organisations:
            organisations.append(date_and_organisations[i][1])

    for i in range(len(organisations)):
        globals()[f'ls_{i}'] = []
        for j in range(len(dates)):
            if (dates[j], organisations[i]) in date_and_organisations:
                for k in range(len(date_and_organisations)):
                    if (dates[j], organisations[i]) == date_and_organisations[k]:
                        globals()[f'ls_{i}'].append(number_of_orders_by_organization[k])
            else:
                if (dates[j], organisations[i]) not in date_and_organisations:
                    globals()[f'ls_{i}'].append(0)

    # Установить ширину полосы
    barWidth = 0.15
    # fig, ax = plt.subplots(figsize=(14.9, 7))
    fig2 = plt.figure(figsize=(14.9, 7))
    # Установить положение стержня по оси X
    # br0 = np.arange(len(dates))
    for i in range(0, len(organisations)):
        if i == 0:
            globals()[f'br{i}'] = np.arange(len(dates))
        else:
            globals()[f'br{i}'] = [x + barWidth for x in globals()[f'br{i - 1}']]

    for i in range(len(organisations)):
        plt.bar(globals()[f'br{i}'], globals()[f'ls_{i}'], color=(random.random(), random.random(), random.random()),
                width=barWidth,
                edgecolor='grey', label=organisations[i])

    # Добавление Xticks и Yticks
    plt.title('Количество заказов (по заведениям)', fontsize=18, color='b')
    plt.xlabel('Дата', fontweight='bold', fontsize=14)
    plt.ylabel('Количество заказов (по заведениям)', fontweight='bold', fontsize=14)
    plt.xticks([r + barWidth for r in range(len(dates))], dates, fontsize=10)
    plt.yticks(fontsize=10)
    plt.gcf().autofmt_xdate()
    plt.legend(fontsize=8)
    fig2.savefig('static/Analytics_Number_of_orders_by_organization.png')

    # Количество заказов за все время по заведениям (по заведениям)
    list_organizations_total_orders = []
    for i in range(len(organisations)):
        # globals()[f'Organizations_total_orders_{i}'] = sum(globals()[f'ls_{i}'])
        list_organizations_total_orders.append(sum(globals()[f'ls_{i}']))

    # Количество заказов за все время
    total_orders = sum(list_organizations_total_orders)
    fig_orders = px.pie(values=list_organizations_total_orders, names=organisations,
                        color_discrete_sequence=px.colors.sequential.RdBu, width=1490, height=700,
                        title="Количество заказов за все время по заведениям (по заведениям)")

    fig_orders.update_traces(textposition='outside',
                             textinfo='percent+label+value',
                             marker=dict(line=dict(color='#FFFFFF')),
                             textfont_size=14)

    fig_orders.update_layout(title_text='Количество заказов за все время по заведениям (по заведениям)', title_x=0.5, font=dict(
        size=16,
        color='#0000FF'
    ))

    fig_orders.write_image('static/Number_of_orders_for_all_time_by_organization.png')

    list_date_order = list(set(date_orders))
    list_date_orders = sorted([a for a in list_date_order])

    id_organisation = db.query(Order.id).filter(Order.unit_id != 1).filter(Order.unit_id != 2).filter(Order.unit_id != 3).all()
    id_organisations = sorted([a[0] for a in id_organisation])
    date_organisation = db.query(Order.date).filter(Order.unit_id != 1).filter(Order.unit_id != 2).filter(Order.unit_id != 3).all()
    date_organisations = sorted([a[0].strftime('%Y/%m/%d') for a in date_organisation])

    # Аналитика по периодам


    return templates.TemplateResponse('analytics.html', context={'request': request, 'array_result': array_result, 'id_orders': id_orders,
                                                                 'date_orders': date_orders, 'unit_id_organisations': unit_id_organisations,
                                                                 'name_organisations': name_organisations,
                                                                 'list_date_orders': list_date_orders,
                                                                 'dict_date_and_organisations': dict_date_and_organisations,
                                                                 'values': values, 'counts': counts,
                                                                 'order_tests': order_tests, 'date_tests': array_date_test,
                                                                 'order_canceled': list_order_canceleds,
                                                                 'date_order_canceleds': date_order_canceleds,
                                                                 'array_order_canceleds': array_canceleds, 'array_total': array_total,
                                                                 'id_organisation': id_organisations, 'date_organisations': date_organisations,
                                                                 'total_orders': total_orders})
