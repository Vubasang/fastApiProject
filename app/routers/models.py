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

