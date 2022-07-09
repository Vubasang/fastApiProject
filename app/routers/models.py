from sqlalchemy import Column, DateTime, BigInteger, VARCHAR, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Statusorder(Base):
    __tablename__ = 'orders_statusorder'
    id = Column(BigInteger, primary_key=True)
    status = Column(VARCHAR(120))
    created = Column(TIMESTAMP)


class Order(Base):
    __tablename__ = 'orders_order'
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime(timezone=True))

    # statusorder_id = Column(VARCHAR(120), ForeignKey('orders_statusorder.id'))
    # orders_statusorder = relationship(Statusorder, backref=backref('orders_orders', uselist=True))