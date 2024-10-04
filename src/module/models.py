from sqlalchemy import Boolean, Float, Integer, Column, String,DateTime, ForeignKey
from src.database.core import Base


class DBModule(Base):
    __tablename__ = 'Module'
    module_code = Column(String(100), unique=True, primary_key=True)
    module_name = Column(String(100), unique=True)  # human-readable
    module_location = Column(String(1000), unique=True)  # TODO: better way to store location (for graphing)
    module_status = Column(Integer)
    last_received_signal_date = Column(DateTime)
    signal_power = Column(Float)
