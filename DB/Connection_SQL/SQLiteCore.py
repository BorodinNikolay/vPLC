from datetime import datetime
from peewee import *

SqliteDB = SqliteDatabase("SQLite.db")


class SQL_tag(Model):
    id = PrimaryKeyField(unique=True)
    time = DateTimeField(default=datetime.now)
    valueInt = IntegerField(null=True)
    valueReal = FloatField(null=True)
    valueBool = BooleanField(null=True)

    class Meta:
        database = SqliteDB
        db_table = "Hello"


if __name__ == '__main__':
    SQL_tag.create_table()
