import time
from PyQt6.QtCore import QThread, pyqtSignal
from datetime import datetime
from peewee import *

# if __name__ == '__main__':
#     SqliteDB = SqliteDatabase("SQLite.db")
# else:
#     SqliteDB = SqliteDatabase("DB/SQLite.db")

SqliteDB = SqliteDatabase("DB/SQLite.db")


class SQL_tag(Model):
    id = PrimaryKeyField(unique=True)
    time = DateTimeField(default=datetime.now)
    valueInt = IntegerField(null=True)
    valueReal = FloatField(null=True)
    valueBool = BooleanField(null=True)

    class Meta:
        database = SqliteDB
        order_by = "-id"


class Tag:
    def __init__(self, value=None, name="", comment="", retain=False, dataType=None, OPC=False, SQL=False):
        self.value = value
        self.retain = retain
        self.dataType = dataType
        self.name = name
        self.comment = comment
        self.OPC = OPC
        self.SQL = SQL
        self.SQLTable = None
        if SQL:
            self.SQLTable = type(self.name, (SQL_tag,), {})
            self.SQLTable._meta.table_name = self.name
            self.SQLTable.create_table()

    def setValue(self, value):
        self.value = value
        if self.SQLTable:
            if isinstance(value, int):
                # print(value)
                self.SQLTable(valueInt=value).save()

    def getValue(self):
        return self.value


class Refresh(QThread):
    refreshSignal = pyqtSignal()

    def __init__(self, refreshTime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refreshTime = refreshTime

    def run(self):
        while True:
            self.refreshSignal.emit()
            print("Refresh")
            time.sleep(self.refreshTime)


class OB(QThread):
    refreshSignal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def loop(self):
        pass

    def run(self):
        while True:
            self.loop()
            time.sleep(0.01)


# FUNCTIONS

def lamp24control(value, *args):
    _num = round(((value.getValue() - 4000) / 160) / 100 * len(args))
    for i, v in enumerate(args):
        if i <= _num - 1:
            v.setValue(True)
        else:
            v.setValue(False)
