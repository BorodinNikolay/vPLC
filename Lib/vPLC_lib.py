import time
from PyQt6.QtCore import QThread, pyqtSignal
from datetime import datetime
from peewee import *

SqliteDB = SqliteDatabase("DB/SQLite.db", pragmas={
    'journal_mode': 'wal',
    'synchronous': 0,
    'cache_size': -32000
    })


class SQL_tag(Model):
    id = PrimaryKeyField(unique=True)
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = SqliteDB
        # order_by = "-id"


class SQL_tagINT(SQL_tag):
    value = IntegerField(null=True)

class SQL_tagFLOAT(SQL_tag):
    value = FloatField(null=True)

class SQL_tagBOOL(SQL_tag):
    value = BooleanField(null=True)

class SQL_tagSTR(SQL_tag):
    value = TextField(null=True)

class SQL_tagANY(SQL_tag):
    value = AnyField(null=True)






class Tag:
    def __init__(self, value=None, name="", comment="", retain=False, dataType=None, OPC=False, SQL=False):
        self.value = value
        self.__valuePrevious = None
        self.retain = retain
        self.dataType = dataType
        self.name = name
        self.comment = comment
        self.OPC = OPC
        self.SQL = SQL
        self.SQLTableModel = None
        # Включить логирование в SQL если включена настройка retain
        if self.retain and not self.SQL:
            self.SQL = True
        # Создание таблицы с рдноименным названием тэга в SQL
        if self.SQL:
            self.createSQLTable()
        # Считываение с SQL и присвоение переменной. Реализация retain
        if self.retain:
            try:
                self.retainRead()
            except:
                self.setValue(value)
        else:
            self.setValue(value)



    def retainRead(self):
        _table = self.SQLTableModel._meta.table
        _value = _table.select(_table.value).order_by(_table.id.desc()).get()["value"]
        # print(self.name, _value)
        self.setValue(_value)
        # return _value

    def createSQLTable(self):
        if isinstance(self.value, int):
            self.SQLTableModel = type(self.name, (SQL_tagINT,), {})
        elif isinstance(self.value, bool):
            self.SQLTableModel = type(self.name, (SQL_tagBOOL,), {})
        elif isinstance(self.value, float):
            self.SQLTableModel = type(self.name, (SQL_tagFLOAT,), {})
        elif isinstance(self.value, str):
            self.SQLTableModel = type(self.name, (SQL_tagSTR,), {})
        else:
            self.SQLTableModel = type(self.name, (SQL_tagANY,), {})
        self.SQLTableModel._meta.table_name = self.name
        self.SQLTableModel.create_table(safe=True)

    def setValue(self, value):
        if isinstance(self.value, bool):
            __value = True if value == 1 else False
        else:
            __value = value

        if __value != self.__valuePrevious:
            self.value = __value
            if self.SQL:
                self.SQLTableModel(value = __value).save()
            self.__valuePrevious = __value

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
