from datetime import datetime
from peewee import *
# from DB.Connection_SQL import connection_SQL_DB
# from DB.SQL_models.base import *


class SQL_PLC_Tags(BaseModel):
    id = PrimaryKeyField(unique=True)
    value = FloatField(null=True)
    time = DateTimeField(default=datetime.now)

    @staticmethod
    def list():
        query = SQL_PLC_Tags.select()
        for row in query:
            print(row.id, row.value, row.time)

    class Meta:
        db = connection_SQL_DB.database
        db_table = "SQL_PLC_Tags"