from sqlalchemy import Column, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders_order'
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime(timezone=True))

