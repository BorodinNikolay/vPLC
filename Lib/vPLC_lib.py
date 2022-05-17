import time

from PyQt6.QtCore import QThread, pyqtSignal


class Tag:
    def __init__(self, value=None, OPC=False, SQL=False):
        self.value = value
        self.OPC = OPC
        self.SQL = SQL

    # def __setattr__(self, key, value):
    #     if key == "value" and value:
    #         print(key, value)

    def setValue(self, value):
        self.value = value
        # print(value)

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
