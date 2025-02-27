import json
import logging
from src.database.core import get_db_session

def unwrap_message(payload:str):
    try:
        message = json.loads(payload)
    except Exception as e:
        logging.info("Error: failed to convert string message to json!")
        return


    with get_db_session() as db:
        pass #TODO: After sensor model and connector refactor