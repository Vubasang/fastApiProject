from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders_order'
    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime(timezone=True))

