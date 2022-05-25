from peewee import Model
from DB.Connection_SQL.connection_SQL_DB import *


class BaseModel(Model):
    class Meta:
        order_by = id  # Сортировка по умолчанию

