from PLC_Tags import *
from PLC_Hardware import *
import threading

Links = [
    MirageNAILink(Module=DIN_rail_1["NAI"], Tag0=PLC_tags["AI0_AO0"], Tag1=PLC_tags["AI1_AO1"],
                  Tag2=PLC_tags["AI2_T_mA"], Tag3=PLC_tags["AI3_NPSI"])
]

if __name__ == "__main__":
    Links[0].syncOnce()
    # my_thread = threading.Thread(target=Links[0].syncOnce())
    # my_thread.start()
