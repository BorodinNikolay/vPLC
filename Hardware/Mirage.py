from pyModbusTCP.client import ModbusClient
from Lib.vPLC_lib import Tag
import time


class MirageBasic(ModbusClient):
    def __init__(self, host=None, port=502, unit_id=None, timeout=None, debug=None, auto_open=True, auto_close=False):
        super().__init__(host, port, unit_id, timeout, debug, auto_open, auto_close)

    def __del__(self):
        self.close()


class MirageNAI(MirageBasic):

    def getValue(self, channel):
        return self.read_holding_registers(channel, 1)[0]

    def getAll(self):
        return self.read_holding_registers(0, 16)


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
    NAI = MirageNAI("192.168.8.192")
    NDI = MirageNDI("192.168.8.195")
    NPT = MirageNPT("192.168.8.193")
    NDO = MirageNDO("192.168.8.194")
    NAO = MirageNAODI("192.168.8.191")

    Peremennaya = Tag()
    a = MirageNAILink(Module=NAI, Tag2=Peremennaya)
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
