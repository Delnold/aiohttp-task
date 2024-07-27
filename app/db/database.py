import logging

from peewee_async import PostgresqlDatabase, Manager
from app.core.config import db_settings

logging.basicConfig(level=logging.DEBUG)
database = PostgresqlDatabase(
    database=db_settings.db_name,
    user=db_settings.db_user,
    password=db_settings.db_pass,
    host=db_settings.db_host,
    port=db_settings.db_port
)

def close():
    if not database.is_closed():
        database.close()

objects = Manager(database)
database.set_allow_sync(True)
