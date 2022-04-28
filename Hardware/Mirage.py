from pyModbusTCP.client import ModbusClient
import time


# 191 - NAO+NDI, 192 - NAI, 193 - NPT, 194 - NDO, 195 - NDI



# c = ModbusClient(host="192.168.8.220", port=502, unit_id=1, auto_open=True, auto_close=False)
# regs = c.read_holding_registers(0, 10)
# lastval = 0
# lasttime = 0
# newtime = 0
# while True:
#     regs = c.read_holding_registers(0, 1)
#     T = ((regs[0]/1000 - 4)/16)*180
#     newtime = time.time()
#     if lasttime == 0:
#         lasttime = newtime
#     if T != lastval:
#         lastval = T
#         print(newtime - lasttime, T)
#         lasttime = newtime


class MirageNAI(ModbusClient):
    def __init__(self, host=None, port=502, unit_id=None, timeout=None, debug=None, auto_open=True, auto_close=True):
        super().__init__(host, port, unit_id, timeout, debug, auto_open, auto_close)

    def _timeTrack(func):
        def wrapper(*args, **kwargs):
            startTime = time.time()
            result = func(*args, **kwargs)
            endTime = time.time()
            deltaTime = round(endTime-startTime, 4)
            print(f"Функция выполнялась {deltaTime}")
            return result
        return wrapper

    # @_timeTrack
    def getValue(self, channel):
        return self.read_holding_registers(channel, 1)[0]

    # @_timeTrack
    def getAll(self):
        return self.read_holding_registers(0, 16)
    

    def __del__(self):
        self.close()




if __name__ == "__main__":
    c = MirageNAI(host="192.168.8.192")

    def multichannel():
        for i in range(16):
            print(c.getValue(i))



    # print(c.getValue(2))

    print(c.getAll())

        