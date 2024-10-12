# models.py
from sqlalchemy import Column, String, Integer
from database import Base

class URLMapping(Base):
    __tablename__ = "urls"

    short_url = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    click_count = Column(Integer, default=0)

class ReusePool(Base):
    __tablename__ = "reuse_pool"
    id = Column(Integer, primary_key=True, index=True)
    short_url = Column(String, unique=True, index=True)