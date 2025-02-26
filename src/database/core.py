from contextlib import contextmanager

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from config import Settings

sett = Settings()

engine = create_engine(sett.db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def _check_if_table_exists(table_name: str):
    return engine.dialect.has_table(engine.connect(), table_name)


def check_all_tables():
    return [_check_if_table_exists(table_name) for table_name in Base.metadata.tables.keys()]


def create_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    session.commit()
    session.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()
