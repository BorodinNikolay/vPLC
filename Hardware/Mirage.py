from pyModbusTCP.client import ModbusClient
import time


# 191 - NAO+NDI, 192 - NAI, 193 - NPT, 194 - NDO, 195 - NDI

class MirageBasic(ModbusClient):
    def __init__(self, host=None, port=502, unit_id=None, timeout=None, debug=None, auto_open=True, auto_close=False):
        super().__init__(host, port, unit_id, timeout, debug, auto_open, auto_close)


    def __del__(self):
        self.close()

    # def _timeTrack(func):
    #     def wrapper(*args, **kwargs):
    #         startTime = time.time()
    #         result = func(*args, **kwargs)
    #         endTime = time.time()
    #         deltaTime = round(endTime - startTime, 4)
    #         print(f"Функция выполнялась {deltaTime}")
    #         return result
    #     return wrapper


class MirageNAI(MirageBasic):

    def getValue(self, channel):
        return self.read_holding_registers(channel, 1)[0]

    def getAll(self):
        return self.read_holding_registers(0, 16)


class MirageNDI(MirageBasic):

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

    def setChannel(self, channel, value):
        val = 0
        if value == True:
            val = 1
        self.write_single_register(1000 + channel, val)


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


if __name__ == "__main__":
    NAI = MirageNAI(host="192.168.8.192")
    NDI = MirageNDI(host="192.168.8.195")
    NPT = MirageNPT(host="192.168.8.193")
    NDO = MirageNDO(host="192.168.8.194")
    NAO = MirageNAODI(host="192.168.8.191")

    print(NAI.getAll())
    print(NDI.getAll())
    print(NPT.getAll())
    print(NDO.getAll())
    print(NAO.getAllDI())

    # for i in range(100):
    #     for j in range(24):
    #         NDO.setChannel(j, True)
    #     for j in range(24):
    #         NDO.setChannel(j, False)
