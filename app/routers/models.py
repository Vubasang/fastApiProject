from sqlalchemy import Column, DateTime, BigInteger, VARCHAR, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders_order'
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime(timezone=True))
    unit_id = Column(BigInteger)
    # statusorder_id = Column(VARCHAR(120), ForeignKey('orders_statusorder.id'))
    # orders_statusorder = relationship(Statusorder, backref=backref('orders_orders', uselist=True))


class Statusorder(Base):
    __tablename__ = 'orders_statusorder'
    id = Column(BigInteger, primary_key=True)
    order_id = Column(BigInteger)
    status = Column(VARCHAR(120))
    created = Column(TIMESTAMP)


class Organisations(Base):
    __tablename__ = 'organisations_organisation'
    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(100))

class Couriers(Base):
    __tablename__ = 'users_user'
    id = Column(BigInteger, primary_key=True)
    first_name = Column(VARCHAR(30))
    last_name = Column(VARCHAR(30))
    middle_name = Column(VARCHAR(30))
