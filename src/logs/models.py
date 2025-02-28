from sqlalchemy import Column, Integer, String, DateTime
from src.database.core import Base


class DBLog(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    message = Column(String(1000))
    timestamp = Column(DateTime)
