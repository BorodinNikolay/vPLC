import time

from Lib.vPLC_lib import *
from DB.DB import DB


class OB1(OB):

    def loop(self):
        if DB["220DI2_2KeyRight"].getValue():
            lamp24control(DB["AI0_AO0"], DB["DO0_NAODI_6_7"], DB["DO1_NAODI_5"], DB["DO2_Lamp"], DB["DO3"], DB["DO4"],
                          DB["DO5"], DB["DO6"], DB["DO7"], DB["DO8"], DB["DO9"], DB["DO10"], DB["DO11"], DB["DO12"],
                          DB["DO13"], DB["DO14"], DB["DO15"], DB["DO16"], DB["DO17"], DB["DO18"], DB["DO19"],
                          DB["DO20"], DB["DO21"], DB["DO22"], DB["DO23"])

        if DB["220DI1_2KeyLeft"].getValue():
            lamp24control(DB["AO0_AI0_ITP"], DB["DO0_NAODI_6_7"], DB["DO1_NAODI_5"], DB["DO2_Lamp"], DB["DO3"], DB["DO4"],
                          DB["DO5"], DB["DO6"], DB["DO7"], DB["DO8"], DB["DO9"], DB["DO10"], DB["DO11"], DB["DO12"],
                          DB["DO13"], DB["DO14"], DB["DO15"], DB["DO16"], DB["DO17"], DB["DO18"], DB["DO19"],
                          DB["DO20"], DB["DO21"], DB["DO22"], DB["DO23"])
