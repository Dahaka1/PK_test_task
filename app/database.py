import os

from loguru import logger
from psycopg2 import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

import src.settings
import src.sql_queries

SQLALCHEMY_DATABASE_URL = src.settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# for manually connecting
conn = connect(
    **src.settings.DATABASE_PARAMS
)

conn.autocommit = True


def database_init() -> None:
    """
    Alembic создает таблицы для сущностей, если их нет (при первом запуске БД)
    """
    with conn.cursor() as cursor:
        cursor.execute(src.sql_queries.GET_ALL_TABLES)
        tables = cursor.fetchall()
        if not any(tables):
            for cmd in src.settings.DATABASE_INIT_COMMANDS:
                os.system(cmd)
            logger.info(
                f"There are {src.settings.STANDARD_DB_TABLES_AMOUNT} DB-tables was created"
            )
        elif len(tables) != src.settings.STANDARD_DB_TABLES_AMOUNT:
            logger.error(
                f"Non-standard DB-tables amount was found ({src.settings.STANDARD_DB_TABLES_AMOUNT} are declared)"
            )
        else:
            pass
