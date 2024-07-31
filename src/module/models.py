from sqlalchemy import Integer, Column, String, ForeignKey
from src.database.core import Base


class DBModule(Base):
    __tablename__ = 'Module'
    module_id = Column(Integer, primary_key=True, autoincrement=True)
    module_name = Column(String(100))
    module_code = Column(String(100))
    location = Column(String(1000))
    is_active = Column(Integer)
    is_deleted = Column(Integer)
    signal_power = Column(Integer)
    url = Column(String)
