# from Lib.vPLC_lib import Tag
from Connection_SQL.SQLiteCore import *


class Tag:
    def __init__(self, value=None, OPC=False, SQL=False):
        self.value = value
        self.OPC = OPC
        self.SQL = SQL
        self.TagName = None
        self.ns = globals()
        print(self.ns)

    # def __setattr__(self, key, value):
    #     if key == "value" and value:
    #         print(key, value)

    def setValue(self, value):
        self.value = value
        # print(self.getClassVariableName())

    def getValue(self):
        return self.value

    def getClassVariableName(self):
        for i, j in globals().items():
            print(i, j)
            if j is self:
                return i


PLC_Tags = {
    # "AI0_AO0": Tag(value=0),
    # "AI1_AO1": Tag(value=0),
    # "AI2_T_mA": Tag(value=0),
    "AI3_NPSI": Tag(value=0),
    # "220DI0_220V": Tag(),
    # "220DI1_2KeyLeft": Tag(),
    # "220DI2_2KeyRight": Tag(),
    # "PT0_T(50m)": Tag(),
    # "PT1_Rheostat": Tag(),
    # "DO0_NAODI_6_7": Tag(),
    # "DO1_NAODI_5": Tag(),
    # "DO2_Lamp": Tag(value=False),
    # "DO3": Tag(),
    # "DO4": Tag(),
    # "DO5": Tag(),
    # "DO6": Tag(),
    # "DO7": Tag(),
    # "DO8": Tag(),
    # "DO9": Tag(),
    # "DO10": Tag(),
    # "DO11": Tag(),
    # "DO12": Tag(),
    # "DO13": Tag(),
    # "DO14": Tag(),
    # "DO15": Tag(),
    # "DO16": Tag(),
    # "DO17": Tag(),
    # "DO18": Tag(),
    # "DO19": Tag(),
    # "DO20": Tag(),
    # "DO21": Tag(),
    # "DO22": Tag(),
    # "DO23": Tag(),
    # "24DI0_220V": Tag(),
    # "24DI1_Button": Tag(),
    # "24DI2_1KeyLeft": Tag(),
    # "24DI3_1KeyRight": Tag(),
    # "24DI5_NDO1": Tag(),
    # "24DI6_NDO0": Tag(),
    # "24DI7_NDO0_invert": Tag(),
    # "AO0_AI0_ITP": Tag(value=0),
    # "AO1_AI1": Tag()
}

if __name__ == '__main__':
    # print(globals())
    # print(locals())
    # SQL_tag.create_table()
    pass
