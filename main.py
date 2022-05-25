import sys
import time
from functools import partial

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon, QColor, QIntValidator
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6 import uic
from UI import ui_vPLC
from Hardware import Mirage
from qt_material import apply_stylesheet
from Lib.vPLC_lib import *
from DB.DB import PLC_Tags
from OB.OB1 import OB1


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui_vPLC.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("vPLC")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon('Graphics/ico.png'))
        self.statusBar()

        self.NAI = Mirage.MirageNAI(host="192.168.8.192", Ch0=PLC_Tags["AI0_AO0"], Ch1=PLC_Tags["AI1_AO1"], Ch2=PLC_Tags["AI2_T_mA"],
                                    Ch3=PLC_Tags["AI3_NPSI"])
        self.NAI.start()
        self.NAI.signal.connect(self.refreshScreenData)

        self.NDI = Mirage.MirageNDI(host="192.168.8.195", Ch0=PLC_Tags["220DI0_220V"], Ch1=PLC_Tags["220DI1_2KeyLeft"],
                                    Ch2=PLC_Tags["220DI2_2KeyRight"])
        self.NDI.start()
        self.NDI.signal.connect(self.refreshScreenData)

        self.NDO = Mirage.MirageNDO(host="192.168.8.194", Ch0=PLC_Tags["DO0_NAODI_6_7"], Ch1=PLC_Tags["DO1_NAODI_5"],
                                    Ch2=PLC_Tags["DO2_Lamp"], Ch3=PLC_Tags["DO3"], Ch4=PLC_Tags["DO4"], Ch5=PLC_Tags["DO5"], Ch6=PLC_Tags["DO6"],
                                    Ch7=PLC_Tags["DO7"], Ch8=PLC_Tags["DO8"], Ch9=PLC_Tags["DO9"], Ch10=PLC_Tags["DO10"],
                                    Ch11=PLC_Tags["DO11"], Ch12=PLC_Tags["DO12"], Ch13=PLC_Tags["DO13"], Ch14=PLC_Tags["DO14"],
                                    Ch15=PLC_Tags["DO15"], Ch16=PLC_Tags["DO16"], Ch17=PLC_Tags["DO17"], Ch18=PLC_Tags["DO18"],
                                    Ch19=PLC_Tags["DO19"], Ch20=PLC_Tags["DO20"], Ch21=PLC_Tags["DO21"], Ch22=PLC_Tags["DO22"],
                                    Ch23=PLC_Tags["DO23"])
        self.NDO.start()

        self.NAODI = Mirage.MirageNAODI(host="192.168.8.191", DICh0=PLC_Tags["24DI0_220V"], DICh1=PLC_Tags["24DI1_Button"],
                                        DICh2=PLC_Tags["24DI2_1KeyLeft"], DICh3=PLC_Tags["24DI3_1KeyRight"], DICh5=PLC_Tags["24DI5_NDO1"],
                                        DICh6=PLC_Tags["24DI6_NDO0"], DICh7=PLC_Tags["24DI7_NDO0_invert"],
                                        AOCh0=PLC_Tags["AO0_AI0_ITP"], AOCh1=PLC_Tags["AO1_AI1"])
        self.NAODI.start()
        self.NAODI.signal.connect(self.refreshScreenData)

        self.OB1 = OB1()
        self.OB1.start()

        self.ui.cb0.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO0_NAODI_6_7"]))
        self.ui.cb1.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO1_NAODI_5"]))
        self.ui.cb2.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO2_Lamp"]))
        self.ui.cb3.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO3"]))
        self.ui.cb4.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO4"]))
        self.ui.cb5.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO5"]))
        self.ui.cb6.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO6"]))
        self.ui.cb7.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO7"]))
        self.ui.cb8.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO8"]))
        self.ui.cb9.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO9"]))
        self.ui.cb10.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO10"]))
        self.ui.cb11.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO11"]))
        self.ui.cb12.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO12"]))
        self.ui.cb13.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO13"]))
        self.ui.cb14.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO14"]))
        self.ui.cb15.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO15"]))
        self.ui.cb16.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO16"]))
        self.ui.cb17.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO17"]))
        self.ui.cb18.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO18"]))
        self.ui.cb19.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO19"]))
        self.ui.cb20.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO20"]))
        self.ui.cb21.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO21"]))
        self.ui.cb22.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO22"]))
        self.ui.cb23.toggled.connect(partial(self.checkBox, db=PLC_Tags["DO23"]))

        self.ui.horizontalSlider.valueChanged.connect(partial(self.sliderToDB, db=PLC_Tags["AO0_AI0_ITP"]))
        self.ui.lineEdit.setValidator(QIntValidator(0, 25000))
        self.ui.lineEdit.returnPressed.connect(partial(self.lineEditToDB, db=PLC_Tags["AO1_AI1"]))

    def refreshScreenData(self):
        self.ui.AI0.setText(str(PLC_Tags["AI0_AO0"].getValue()))
        self.ui.AI1.setText(str(PLC_Tags["AI1_AO1"].getValue()))
        self.ui.AI2.setText(str(float('{:.1f}'.format((((PLC_Tags["AI2_T_mA"].getValue() - 4000) / 160)) - 50))) + " °C")
        self.ui.AI3.setText(str(float('{:.1f}'.format((PLC_Tags["AI3_NPSI"].getValue() - 4000) / 160))) + " %")

        self.ui.progressBar_2.setRange(4000, 20000)
        self.ui.progressBar_2.setValue(PLC_Tags["AI0_AO0"].getValue())

        self.ui.progressBar_3.setRange(4000, 20000)
        self.ui.progressBar_3.setValue(PLC_Tags["AI1_AO1"].getValue())

        self.ui.progressBar_4.setRange(4000, 20000)
        self.ui.progressBar_4.setValue(PLC_Tags["AI2_T_mA"].getValue())

        self.ui.progressBar.setRange(4000, 20000)
        self.ui.progressBar.setValue(PLC_Tags["AI3_NPSI"].getValue())

        if PLC_Tags["220DI0_220V"].getValue():
            self.ui._220DI0.setStyleSheet("background-color: Lime")
        else:
            self.ui._220DI0.setStyleSheet("background-color: red")

        if PLC_Tags["220DI1_2KeyLeft"].getValue():
            self.ui._220DI1.setStyleSheet("background-color: Lime")
        else:
            self.ui._220DI1.setStyleSheet("background-color: red")

        if PLC_Tags["220DI2_2KeyRight"].getValue():
            self.ui._220DI2.setStyleSheet("background-color: Lime")
        else:
            self.ui._220DI2.setStyleSheet("background-color: red")

        if PLC_Tags["24DI0_220V"].getValue():
            self.ui._24DI0.setStyleSheet("background-color: Lime")
        else:
            self.ui._24DI0.setStyleSheet("background-color: red")

        if PLC_Tags["24DI1_Button"].getValue():
            self.ui._24DI1.setStyleSheet("background-color: Lime")
        else:
            self.ui._24DI1.setStyleSheet("background-color: red")

        if PLC_Tags["24DI2_1KeyLeft"].getValue():
            self.ui._24DI2.setStyleSheet("background-color: Lime")
        else:
            self.ui._24DI2.setStyleSheet("background-color: red")

        if PLC_Tags["24DI3_1KeyRight"].getValue():
            self.ui._24DI3.setStyleSheet("background-color: Lime")
        else:
            self.ui._24DI3.setStyleSheet("background-color: red")

        if PLC_Tags["24DI5_NDO1"].getValue():
            self.ui._24DI5.setStyleSheet("background-color: Lime")
        else:
            self.ui._24DI5.setStyleSheet("background-color: red")

        if PLC_Tags["24DI6_NDO0"].getValue():
            self.ui._24DI6.setStyleSheet("background-color: Lime")
        else:
            self.ui._24DI6.setStyleSheet("background-color: red")

        if PLC_Tags["24DI7_NDO0_invert"].getValue():
            self.ui._24DI7.setStyleSheet("background-color: Lime")
        else:
            self.ui._24DI7.setStyleSheet("background-color: red")

    def checkBox(self, state, db):
        db.setValue(state)

    def sliderToDB(self, value, db):
        db.setValue(value * 160 + 4000)

    def lineEditToDB(self, db):
        db.setValue(int(self.ui.lineEdit.text()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    apply_stylesheet(app, theme="dark_cyan.xml", invert_secondary=False)

    window.show()
    sys.exit(app.exec())
