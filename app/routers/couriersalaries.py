from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import DateTime

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

    if(dateSelected):
        resultt = 'Зарплата у каждого курьера на ' + dateSelected + ' составляет:'
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

        date_test = db.query(Order.date).filter(
            (Order.unit_id == 1) | (Order.unit_id == 2) | (Order.unit_id == 3)).all()
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
        c_date = collections.Counter(array_result) - collections.Counter(array_date_test) - collections.Counter(
            array_canceleds)
        values = []
        counts = []
        for value, key in c_date.items():
            values.append(value)
            counts.append(key)


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
            plt.bar(globals()[f'br{i}'], globals()[f'ls_{i}'],
                    color=(random.random(), random.random(), random.random()),
                    width=barWidth,
                    edgecolor='grey', label=organisations[i])

        # Количество заказов за все время по заведениям (по заведениям)
        list_organizations_total_orders = []
        for i in range(len(organisations)):
            # globals()[f'Organizations_total_orders_{i}'] = sum(globals()[f'ls_{i}'])
            list_organizations_total_orders.append(sum(globals()[f'ls_{i}']))

        # Количество заказов за все время
        total_orders = sum(list_organizations_total_orders)

        list_date_order = list(set(date_orders))
        list_date_orders = sorted([a for a in list_date_order])

        id_organisation = db.query(Order.id).filter(Order.unit_id != 1).filter(Order.unit_id != 2).filter(
            Order.unit_id != 3).all()
        id_organisations = sorted([a[0] for a in id_organisation])
        date_organisation = db.query(Order.date).filter(Order.unit_id != 1).filter(Order.unit_id != 2).filter(
            Order.unit_id != 3).all()
        date_organisations = sorted([a[0].strftime('%Y/%m/%d') for a in date_organisation])

        # Зарплата у курьеров по дням
        id_courier = []
        for i in id_orders:
            id_courier.append(db.query(Order.courier_id).filter(Order.id == i).all())
        id_couriers = [a[0][0] for a in id_courier]

        delivery_cost = []
        for i in id_orders:
            delivery_cost.append(db.query(Order.delivery_cost).filter(Order.id == i).all())
        delivery_costs = [a[0][0] for a in delivery_cost]

        first_name_courier = []
        for i in id_couriers:
            first_name_courier.append(db.query(Couriers.first_name).filter(Couriers.id == i).all())
        first_name_couriers = [a[0][0] for a in first_name_courier]

        last_name_courier = []
        for i in id_couriers:
            last_name_courier.append(db.query(Couriers.last_name).filter(Couriers.id == i).all())
        last_name_couriers = [a[0][0] for a in last_name_courier]

        middle_name_courier = []
        for i in id_couriers:
            middle_name_courier.append(db.query(Couriers.middle_name).filter(Couriers.id == i).all())
        middle_name_couriers = [a[0][0] for a in middle_name_courier]

        full_name_couriers = []
        for i in range(len(first_name_couriers)):
            full_name_couriers.append(first_name_couriers[i] + ' ' + last_name_couriers[i] + ' ' + middle_name_couriers[i])

        dict_date_and_courier = list(zip(date_orders, full_name_couriers, id_couriers))

        list_date_and_courier = list(set(dict_date_and_courier))
        list_date_and_couriers = sorted([a for a in list_date_and_courier])

        salaries = []
        for i in range(len(list_date_and_couriers)):
            salaries.append(0)

        for i in range(len(list_date_and_couriers)):
            for j in range(len(dict_date_and_courier)):
                if dict_date_and_courier[j] == list_date_and_couriers[i]:
                    salaries[i] += delivery_costs[j]

        print(dateSelected)
        k = datetime.strptime(dateSelected, "%Y-%m-%d").strftime('%Y/%m/%d')
        print(k)

        fullname_by_date = []
        id_couriers_by_date = []
        salaries_couriers_by_date = []

        for i in range(len(list_date_and_couriers)):
            if list_date_and_couriers[i][0] == k:
                fullname_by_date.append(list_date_and_couriers[i][1])
                id_couriers_by_date.append(list_date_and_couriers[i][2])
                salaries_couriers_by_date.append(salaries[i])

    else:
        resultt = "Пожалуйста выберите правильную дату"

    return templates.TemplateResponse('couriersalaries.html', context={'request': request, 'dateSelected': dateSelected, 'resultt': resultt,
                                                                       'array_result': array_result,
                                                                       'id_orders': id_orders,
                                                                       'date_orders': date_orders,
                                                                       'unit_id_organisations': unit_id_organisations,
                                                                       'name_organisations': name_organisations,
                                                                       'list_date_orders': list_date_orders,
                                                                       'dict_date_and_organisations': dict_date_and_organisations,
                                                                       'values': values, 'counts': counts,
                                                                       'order_tests': order_tests,
                                                                       'date_tests': array_date_test,
                                                                       'order_canceled': list_order_canceleds,
                                                                       'date_order_canceleds': date_order_canceleds,
                                                                       'array_order_canceleds': array_canceleds,
                                                                       'array_total': array_total,
                                                                       'id_organisation': id_organisations,
                                                                       'date_organisations': date_organisations,
                                                                       'total_orders': total_orders,
                                                                       'id_couriers': id_couriers,
                                                                       'first_name_couriers': first_name_couriers,
                                                                       'last_name_couriers': last_name_couriers,
                                                                       'middle_name_couriers': middle_name_couriers,
                                                                       'full_name_couriers': full_name_couriers,
                                                                       'dict_date_and_courier': dict_date_and_courier,
                                                                       'delivery_costs': delivery_costs,
                                                                       'list_date_and_couriers': list_date_and_couriers,
                                                                       'salaries': salaries,
                                                                       'fullname_by_date': fullname_by_date,
                                                                       'id_couriers_by_date': id_couriers_by_date,
                                                                       'salaries_couriers_by_date': salaries_couriers_by_date}
    )
