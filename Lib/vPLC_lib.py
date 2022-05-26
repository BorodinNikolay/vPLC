import time

import self
from PyQt6.QtCore import QThread, pyqtSignal
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
        order_by = "id"


class Tag(SQL_tag):
    def __init__(self, value=None, name="", comment="", retain=False, dataType=None, OPC=False, SQL=False):
        super().__init__()
        self.value = value
        self.retain = retain
        self.dataType = dataType
        self.name = name
        self.comment = comment
        self.OPC = OPC
        self.SQL = SQL
        self._meta.table_name = self.name

        self.create_table()

    class Meta:
        pass


    # def __setattr__(self, key, value):
    #     if key == "value" and value:
    #         print(key, value)

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def getClassVariableName(self):
        for i, j in globals().items():
            print(i, j)
            if j is self:
                return i


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
