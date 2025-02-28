from datetime import datetime

from src.database.core import get_db_session
from src.logs.connector import create_new_log

class Logger:
    @staticmethod
    def write(message):
        timestamp = datetime.now()
        with get_db_session() as db:
            create_new_log(db,message,timestamp)
