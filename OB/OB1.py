import time

from Lib.vPLC_lib import *
from DB.DB import PLC_Tags


class OB1(OB):

    def loop(self):
        if PLC_Tags["220DI2_2KeyRight"].getValue():
            lamp24control(PLC_Tags["AI0_AO0"], PLC_Tags["DO0_NAODI_6_7"], PLC_Tags["DO1_NAODI_5"], PLC_Tags["DO2_Lamp"], PLC_Tags["DO3"], PLC_Tags["DO4"],
                          PLC_Tags["DO5"], PLC_Tags["DO6"], PLC_Tags["DO7"], PLC_Tags["DO8"], PLC_Tags["DO9"], PLC_Tags["DO10"], PLC_Tags["DO11"], PLC_Tags["DO12"],
                          PLC_Tags["DO13"], PLC_Tags["DO14"], PLC_Tags["DO15"], PLC_Tags["DO16"], PLC_Tags["DO17"], PLC_Tags["DO18"], PLC_Tags["DO19"],
                          PLC_Tags["DO20"], PLC_Tags["DO21"], PLC_Tags["DO22"], PLC_Tags["DO23"])

        if PLC_Tags["220DI1_2KeyLeft"].getValue():
            lamp24control(PLC_Tags["AO0_AI0_ITP"], PLC_Tags["DO0_NAODI_6_7"], PLC_Tags["DO1_NAODI_5"], PLC_Tags["DO2_Lamp"], PLC_Tags["DO3"], PLC_Tags["DO4"],
                          PLC_Tags["DO5"], PLC_Tags["DO6"], PLC_Tags["DO7"], PLC_Tags["DO8"], PLC_Tags["DO9"], PLC_Tags["DO10"], PLC_Tags["DO11"], PLC_Tags["DO12"],
                          PLC_Tags["DO13"], PLC_Tags["DO14"], PLC_Tags["DO15"], PLC_Tags["DO16"], PLC_Tags["DO17"], PLC_Tags["DO18"], PLC_Tags["DO19"],
                          PLC_Tags["DO20"], PLC_Tags["DO21"], PLC_Tags["DO22"], PLC_Tags["DO23"])
