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

    def getClassVariableName(self):
        for i, j in globals().items():
            if j is self:
                return i

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
        print("Run")
        while True:
            self.getAll()


class MirageNDI(MirageBasic):

    def getValue(self, channel):
        if self.read_holding_registers(1000 + channel, 1) == [0]:
            return False
        else:
            return True

    def getAll(self):
        raw = self.read_holding_registers(1000, 24)
        result = []
        for i in raw:
            if i == 0:
                result.append(False)
            else:
                result.append(True)
        return result


class MirageNPT(MirageBasic):

    def getValue(self, channel):
        return self.read_holding_registers(channel, 1)[0]

    def getAll(self):
        return self.read_holding_registers(0, 8)


class MirageNDO(MirageBasic):

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
        if value:
            val = 1
        self.write_single_register(1000 + channel, val)

    def setAll(self, value):
        if value:
            val = [1] * 24
        else:
            val = [0] * 24
        self.write_multiple_registers(1000, val)


class MirageNAODI(MirageBasic):

    def getAllDI(self):
        raw = self.read_holding_registers(16, 8)
        result = []
        for i in raw:
            if i == 0:
                result.append(False)
            else:
                result.append(True)
        return result

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


class MirageNAILink:
    def __init__(self, Module: MirageNAI = None, Tag0: Tag = None, Tag1: Tag = None, Tag2: Tag = None, Tag3: Tag = None,
                 Tag4: Tag = None, Tag5: Tag = None, Tag6: Tag = None,
                 Tag7: Tag = None, Tag8: Tag = None, Tag9: Tag = None, Tag10: Tag = None, Tag11: Tag = None,
                 Tag12: Tag = None, Tag13: Tag = None, Tag14: Tag = None,
                 Tag15: Tag = None):
        self.Module = Module
        self.Tags = [Tag0, Tag1, Tag2, Tag3, Tag4, Tag5, Tag6, Tag7, Tag8, Tag9, Tag10, Tag11, Tag12, Tag13, Tag14,
                     Tag15]

    def syncOnce(self):
        array = self.Module.getAll()
        for _ in self.Tags:
            if _:
                _.setValue(array[self.Tags.index(_)])
                # print(f"Tag{self.Tags.index(_)} значение {array[self.Tags.index(_)]}")

    def syncLoop(self):
        while True:
            self.syncOnce()
            time.sleep(0.1)


if __name__ == "__main__":
    perenemmss = Tag()
    print(perenemmss.getValue())

    NAI = MirageNAI(host="192.168.8.192", Ch3=perenemmss)


    NAI.getAll()
    print(perenemmss.getValue())
    # NAI.start()


    # NDI = MirageNDI("192.168.8.195")
    # NPT = MirageNPT("192.168.8.193")
    # NDO = MirageNDO("192.168.8.194")
    # NAO = MirageNAODI("192.168.8.191")

    # Peremennaya = Tag()
    # a = MirageNAILink(Module=NAI, Tag2=Peremennaya)
    # a.syncOnce()
    # print(NAI.getAll())
    # print(NDI.getAll())
    # print(NPT.getAll())
    # print(NDO.getAll())
    # print(NAO.getAllDI())

    # for _ in range(4000, 20000, 10):
    #     NAO.setValueAO(0, _)
    #     time.sleep(0.1)
    #
    # for _ in range(20000, 4000, -10):
    #     NAO.setValueAO(0, _)
    #     time.sleep(0.1)

    # startTime = time.time()
    # for i in range(100):
    #     for i in range(16):
    #         NAI.getValue(i)
    # print(time.time()-startTime)
    #
    # startTime = time.time()
    # for i in range(100):
    #     NAI.getAll()
    # print(time.time() - startTime)

    # for i in range(100):
    #     for j in range(24):
    #         NDO.setValue(j, True)
    #     for j in range(24):
    #         NDO.setValue(j, False)
