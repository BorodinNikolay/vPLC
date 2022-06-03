from Lib.vPLC_lib import Tag

PLC_Tags = {
    "AI0_AO0": Tag(value=0, name="AI0_AO0", SQL=True),
    "AI1_AO1": Tag(value=0, name="AI1_AO1"),
    "AI2_T_mA": Tag(value=0, name="AI2_T_mA", SQL=True),
    "AI3_NPSI": Tag(value=0, name="AI3_NPSI", SQL=True),
    "220DI0_220V": Tag(),
    "220DI1_2KeyLeft": Tag(),
    "220DI2_2KeyRight": Tag(),
    "PT0_T(50m)": Tag(),
    "PT1_Rheostat": Tag(),
    "DO0_NAODI_6_7": Tag(name="DO0_NAODI_6_7", retain=True),
    "DO1_NAODI_5": Tag(name="DO1_NAODI_5", retain=True),
    "DO2_Lamp": Tag(name="DO2_Lamp", value=False, retain=True),
    "DO3": Tag(name="DO3", retain=True),
    "DO4": Tag(name="DO4", retain=True),
    "DO5": Tag(name="DO5", retain=True),
    "DO6": Tag(name="DO6", retain=True),
    "DO7": Tag(name="DO7", retain=True),
    "DO8": Tag(name="DO8", retain=True),
    "DO9": Tag(name="DO9", retain=True),
    "DO10": Tag(name="DO10", retain=True),
    "DO11": Tag(name="DO11", retain=True),
    "DO12": Tag(name="DO12", retain=True),
    "DO13": Tag(name="DO13", retain=True),
    "DO14": Tag(name="DO14", retain=True),
    "DO15": Tag(name="DO15", retain=True),
    "DO16": Tag(name="DO16", retain=True),
    "DO17": Tag(name="DO17", retain=True),
    "DO18": Tag(name="DO18", retain=True),
    "DO19": Tag(name="DO19", retain=True),
    "DO20": Tag(name="DO20", retain=True),
    "DO21": Tag(name="DO21", retain=True),
    "DO22": Tag(name="DO22", retain=True),
    "DO23": Tag(name="DO23", retain=True),
    "24DI0_220V": Tag(),
    "24DI1_Button": Tag(),
    "24DI2_1KeyLeft": Tag(),
    "24DI3_1KeyRight": Tag(),
    "24DI5_NDO1": Tag(),
    "24DI6_NDO0": Tag(),
    "24DI7_NDO0_invert": Tag(),
    "AO0_AI0_ITP": Tag(value=0, name="AO0_AI0_ITP", retain=True),
    "AO1_AI1": Tag(value=0, name="AO1_AI1", retain=True)
}

