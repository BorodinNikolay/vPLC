from pyModbusTCP.client import ModbusClient
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
        print(f"Значение канала {channel} установлено на {value / 1000} мА. на ИТП должно быть {(value - 4000) / 160}")
        self.write_single_register(channel, value)


if __name__ == "__main__":
    NAI = MirageNAI("192.168.8.192")
    NDI = MirageNDI("192.168.8.195")
    NPT = MirageNPT("192.168.8.193")
    NDO = MirageNDO("192.168.8.194")
    NAO = MirageNAODI("192.168.8.191")

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
