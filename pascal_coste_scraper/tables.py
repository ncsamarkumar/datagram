from sqlalchemy import Column, Integer, DateTime, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    brand = Column(VARCHAR(255))
    productUrl = Column(VARCHAR(255))
    price = Column(VARCHAR(20))
    imageUrl = Column(VARCHAR(255))
    timeStamp = Column(DateTime)
