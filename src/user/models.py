from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.core import Base

class DBUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    keycloak_id = Column(String, unique=True, index=True)
    login = Column(String, unique=True, index=True)