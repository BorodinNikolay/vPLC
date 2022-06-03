from pyModbusTCP.client import ModbusClient
from Lib.vPLC_lib import Tag
from PyQt6.QtCore import QThread, pyqtSignal
import time


class MirageBasic(QThread, ModbusClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port(502)
        self.auto_open(True)
        self.auto_close(False)

    def __del__(self):
        self.close()


class MirageNAI(MirageBasic):
    signal = pyqtSignal()

    def __init__(self, Ch0: Tag = None, Ch1: Tag = None, Ch2: Tag = None, Ch3: Tag = None, Ch4: Tag = None,
                 Ch5: Tag = None, Ch6: Tag = None, Ch7: Tag = None, Ch8: Tag = None, Ch9: Tag = None,
                 Ch10: Tag = None, Ch11: Tag = None, Ch12: Tag = None, Ch13: Tag = None, Ch14: Tag = None,
                 Ch15: Tag = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._Ch = [Ch0, Ch1, Ch2, Ch3, Ch4, Ch5, Ch6, Ch7, Ch8, Ch9, Ch10, Ch11, Ch12, Ch13, Ch14, Ch15]
        self._ChPrevious = None

    def getValue(self, channel):
        return self.read_holding_registers(channel, 1)[0]

    def getAll(self):
        _result = self.read_holding_registers(0, 16)
        _changes = []
        if self._ChPrevious != _result:
            if not self._ChPrevious:
                for i, v in enumerate(_result):
                    if 50 < v < 25000:
                        _changes.append((i, v))
            else:
                for i, v in enumerate(_result):
                    if self._ChPrevious[i] != v and 50 < v < 25000 and abs(self._ChPrevious[i] - v) > 5:
                        _changes.append((i, v))

            for k in _changes:
                # print(k)
                # print(f"Канал {k[0]} новое значение: {k[1]/1000} мА")
                if self._Ch[k[0]]:
                    self._Ch[k[0]].setValue(k[1])
                    self.signal.emit()

            self._ChPrevious = _result
            return _result

    def run(self):
        while True:
            self.getAll()
            # time.sleep(0.001)


class MirageNDI(MirageBasic):
    signal = pyqtSignal()
    def __init__(self, Ch0: Tag = None, Ch1: Tag = None, Ch2: Tag = None, Ch3: Tag = None, Ch4: Tag = None,
                 Ch5: Tag = None, Ch6: Tag = None, Ch7: Tag = None, Ch8: Tag = None, Ch9: Tag = None,
                 Ch10: Tag = None, Ch11: Tag = None, Ch12: Tag = None, Ch13: Tag = None, Ch14: Tag = None,
                 Ch15: Tag = None, Ch16: Tag = None, Ch17: Tag = None, Ch18: Tag = None, Ch19: Tag = None,
                 Ch20: Tag = None, Ch21: Tag = None, Ch22: Tag = None, Ch23: Tag = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._Ch = [Ch0, Ch1, Ch2, Ch3, Ch4, Ch5, Ch6, Ch7, Ch8, Ch9, Ch10, Ch11, Ch12, Ch13, Ch14, Ch15, Ch16, Ch17,
                    Ch18, Ch19, Ch20, Ch21, Ch22, Ch23]
        self._ChPrevious = None

    def getValue(self, channel):
        if self.read_holding_registers(1000 + channel, 1) == [0]:
            return False
        else:
            return True

    def getAll(self):
        raw = self.read_holding_registers(1000, 24)
        _result = []
        for i in raw:
            if i == 0:
                _result.append(False)
            else:
                _result.append(True)

        _changes = []
        if self._ChPrevious != _result:
            if not self._ChPrevious:
                for i, v in enumerate(_result):
                    _changes.append((i, v))
            else:
                for i, v in enumerate(_result):
                    if self._ChPrevious[i] != v:
                        _changes.append((i, v))

            for k in _changes:
                # print(k, self._Ch[k[0]])
                if self._Ch[k[0]]:
                    self._Ch[k[0]].setValue(k[1])
                    self.signal.emit()

            self._ChPrevious = _result
            return _result

    def run(self):
        while True:
            self.getAll()
            # time.sleep(0.001)


class MirageNPT(MirageBasic):

    def getValue(self, channel):
        return self.read_holding_registers(channel, 1)[0]

    def getAll(self):
        return self.read_holding_registers(0, 8)


class MirageNDO(MirageBasic):
    signal = pyqtSignal()

    def __init__(self, Ch0: Tag = None, Ch1: Tag = None, Ch2: Tag = None, Ch3: Tag = None, Ch4: Tag = None,
                 Ch5: Tag = None, Ch6: Tag = None, Ch7: Tag = None, Ch8: Tag = None, Ch9: Tag = None,
                 Ch10: Tag = None, Ch11: Tag = None, Ch12: Tag = None, Ch13: Tag = None, Ch14: Tag = None,
                 Ch15: Tag = None, Ch16: Tag = None, Ch17: Tag = None, Ch18: Tag = None, Ch19: Tag = None,
                 Ch20: Tag = None, Ch21: Tag = None, Ch22: Tag = None, Ch23: Tag = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._Ch = [Ch0, Ch1, Ch2, Ch3, Ch4, Ch5, Ch6, Ch7, Ch8, Ch9, Ch10, Ch11, Ch12, Ch13, Ch14, Ch15, Ch16, Ch17,
                    Ch18, Ch19, Ch20, Ch21, Ch22, Ch23]
        self._ChPrevious = []
        self.signal.emit()

    def getAll(self):
        raw = self.read_holding_registers(1000, 24)
        result = []
        for i in raw:
            if i == 0:
                result.append(False)
            else:
                result.append(True)
        return result

    def getValue(self, channel):
        if self.read_holding_registers(1000 + channel, 1) == [0]:
            return False
        else:
            return True

    def setValue(self, channel, value):
        val = 0
        if value or value != 0:
            val = 1
        self.write_single_register(1000 + channel, val)

    def setAll(self, value):
        if value:
            val = [1] * 24
        else:
            val = [0] * 24
        self.write_multiple_registers(1000, val)

    def syncTags(self):
        _new = [False] * 24
        _changes = []
        # создается _new
        for i, v in enumerate(self._Ch):
            if v and isinstance(v.value, bool):
                _new[i] = v.value
        # Создается список изменений
        if _new != self._ChPrevious:
            if not self._ChPrevious:
                for i, v in enumerate(_new):
                    _changes.append((i, v))
            else:
                for i, v in enumerate(_new):
                    if v != self._ChPrevious[i]:
                        _changes.append((i, v))
        # Присваивается предыдущему значению настоящее
        self._ChPrevious = _new
        # Фильтруется отсутствие изменений
        for i in _changes:
            self.setValue(i[0], i[1])
            self.signal.emit()

    def run(self):
        while True:
            self.syncTags()
            time.sleep(0.001)


class MirageNAODI(MirageBasic):
    signal = pyqtSignal()
    def __init__(self, DICh0: Tag = None, DICh1: Tag = None, DICh2: Tag = None, DICh3: Tag = None, DICh4: Tag = None,
                 DICh5: Tag = None, DICh6: Tag = None, DICh7: Tag = None, AOCh0: Tag = None, AOCh1: Tag = None, AOCh2: Tag = None,
                 AOCh3: Tag = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._Ch = [DICh0, DICh1, DICh2, DICh3, DICh4, DICh5, DICh6, DICh7, AOCh0, AOCh1, AOCh2, AOCh3]
        self._ChPreviousDI = None
        self._ChPreviousAO = None

    def getAllDI(self):
        raw = self.read_holding_registers(16, 8)
        _result = []
        _changes = []
        for i in raw:
            if i == 0:
                _result.append(False)
            else:
                _result.append(True)
        if self._ChPreviousDI != _result:
            if not self._ChPreviousDI:
                for i, v in enumerate(_result):
                    _changes.append((i, v))
            else:
                for i, v in enumerate(_result):
                    if self._ChPreviousDI[i] != v:
                        _changes.append((i, v))

            for k in _changes:
                # print(k, self._Ch[k[0]])
                if self._Ch[k[0]]:
                    self._Ch[k[0]].setValue(k[1])
                    self.signal.emit()

            self._ChPreviousDI = _result
            return _result

    def getAllAO(self):
        return self.read_holding_registers(0, 4)

    def getValueDI(self, channel):
        if self.read_holding_registers(16 + channel, 1) == [0]:
            return False
        else:
            return True

    def getValueAO(self, channel):
        return self.read_holding_registers(channel, 1)[0]

    def setValueAO(self, channel, value):
        self.write_single_register(channel, value)

    def syncTags(self):
        _new = [0] * 4
        _changes = []
        # создается _new
        for i, v in enumerate(self._Ch[8:]):
            if v and isinstance(v.value, int) and 0 < v.value < 25000:
                _new[i] = v.value
        # Создается список изменений
        if _new != self._ChPreviousAO:
            if not self._ChPreviousAO:
                for i, v in enumerate(_new):
                    _changes.append((i, v))
            else:
                for i, v in enumerate(_new):
                    if v != self._ChPreviousAO[i]:
                        _changes.append((i, v))
        # Присваивается предыдущему значению настоящее
        self._ChPreviousAO = _new
        # Фильтруется отсутствие изменений
        for i in _changes:
            # print(i)
            self.setValueAO(i[0], i[1])
            self.signal.emit()


    def run(self):
        while True:
            self.getAllDI()
            self.syncTags()
            # time.sleep(0.0001)




if __name__ == "__main__":
    NAI = MirageNAI(host="192.168.8.192")
    NDI = MirageNDI(host="192.168.8.195")
    NPT = MirageNPT(host="192.168.8.193")
    NDO = MirageNDO(host="192.168.8.194")
    NAO = MirageNAODI(host="192.168.8.191")

