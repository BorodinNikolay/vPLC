import sys
import time
from functools import partial

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6 import uic
from UI import ui_vPLC
from Hardware import Mirage
from qt_material import apply_stylesheet
from Lib.vPLC_lib import *
from DB.DB import DB


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui_vPLC.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("vPLC")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon('Graphics/ico.png'))
        self.statusBar()

        self.NAI = Mirage.MirageNAI(host="192.168.8.192", Ch0=DB["AI0_AO0"], Ch1=DB["AI1_AO1"], Ch3=DB["AI2_T_mA"],
                                    Ch2=DB["AI3_NPSI"])
        self.NAI.start()
        self.NAI.signal.connect(self.refreshScreenData)

        self.NDI = Mirage.MirageNDI(host="192.168.8.195", Ch0=DB["220DI0_220V"], Ch1=DB["220DI1_2KeyLeft"],
                                    Ch2=DB["220DI2_2KeyRight"])
        self.NDI.start()
        self.NDI.signal.connect(self.refreshScreenData)

        self.NDO = Mirage.MirageNDO(host="192.168.8.194", Ch0=DB["DO0_NAODI_6_7"], Ch1=DB["DO1_NAODI_5"],
                                    Ch2=DB["DO2_Lamp"], Ch3=DB["DO3"], Ch4=DB["DO4"], Ch5=DB["DO5"], Ch6=DB["DO6"],
                                    Ch7=DB["DO7"], Ch8=DB["DO8"], Ch9=DB["DO9"], Ch10=DB["DO10"],
                                    Ch11=DB["DO11"], Ch12=DB["DO12"], Ch13=DB["DO13"], Ch14=DB["DO14"],
                                    Ch15=DB["DO15"], Ch16=DB["DO16"], Ch17=DB["DO17"], Ch18=DB["DO18"],
                                    Ch19=DB["DO19"], Ch20=DB["DO20"], Ch21=DB["DO21"], Ch22=DB["DO22"],
                                    Ch23=DB["DO23"])
        self.NDO.start()

        self.ui.cb0.toggled.connect(partial(self.checkBox, db=DB["DO0_NAODI_6_7"]))
        self.ui.cb1.toggled.connect(partial(self.checkBox, db=DB["DO1_NAODI_5"]))
        self.ui.cb2.toggled.connect(partial(self.checkBox, db=DB["DO2_Lamp"]))
        self.ui.cb3.toggled.connect(partial(self.checkBox, db=DB["DO3"]))
        self.ui.cb4.toggled.connect(partial(self.checkBox, db=DB["DO4"]))
        self.ui.cb5.toggled.connect(partial(self.checkBox, db=DB["DO5"]))
        self.ui.cb6.toggled.connect(partial(self.checkBox, db=DB["DO6"]))
        self.ui.cb7.toggled.connect(partial(self.checkBox, db=DB["DO7"]))
        self.ui.cb8.toggled.connect(partial(self.checkBox, db=DB["DO8"]))
        self.ui.cb9.toggled.connect(partial(self.checkBox, db=DB["DO9"]))
        self.ui.cb10.toggled.connect(partial(self.checkBox, db=DB["DO10"]))
        self.ui.cb11.toggled.connect(partial(self.checkBox, db=DB["DO11"]))
        self.ui.cb12.toggled.connect(partial(self.checkBox, db=DB["DO12"]))
        self.ui.cb13.toggled.connect(partial(self.checkBox, db=DB["DO13"]))
        self.ui.cb14.toggled.connect(partial(self.checkBox, db=DB["DO14"]))
        self.ui.cb15.toggled.connect(partial(self.checkBox, db=DB["DO15"]))
        self.ui.cb16.toggled.connect(partial(self.checkBox, db=DB["DO16"]))
        self.ui.cb17.toggled.connect(partial(self.checkBox, db=DB["DO17"]))
        self.ui.cb18.toggled.connect(partial(self.checkBox, db=DB["DO18"]))
        self.ui.cb19.toggled.connect(partial(self.checkBox, db=DB["DO19"]))
        self.ui.cb20.toggled.connect(partial(self.checkBox, db=DB["DO20"]))
        self.ui.cb21.toggled.connect(partial(self.checkBox, db=DB["DO21"]))
        self.ui.cb22.toggled.connect(partial(self.checkBox, db=DB["DO22"]))
        self.ui.cb23.toggled.connect(partial(self.checkBox, db=DB["DO23"]))



    def refreshScreenData(self):
        self.ui.label.setText(str(float('{:.1f}'.format((DB["AI2_T_mA"].getValue() - 4000) / 160))) + " %")
        self.ui.label_2.setText(str(float('{:.1f}'.format((((DB["AI3_NPSI"].getValue() - 4000) / 160)) - 50))) + " °C")
        self.ui.progressBar.setRange(4000, 20000)
        self.ui.progressBar.setValue(DB["AI2_T_mA"].getValue())

        if DB["220DI0_220V"].getValue():
            self.ui._220DI0.setStyleSheet("background-color: green")
        else:
            self.ui._220DI0.setStyleSheet("background-color: red")

        if DB["220DI1_2KeyLeft"].getValue():
            self.ui._220DI1.setStyleSheet("background-color: green")
        else:
            self.ui._220DI1.setStyleSheet("background-color: red")

        if DB["220DI2_2KeyRight"].getValue():
            self.ui._220DI2.setStyleSheet("background-color: green")
        else:
            self.ui._220DI2.setStyleSheet("background-color: red")

    def checkBox(self, state, db):
        db.setValue(state)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    apply_stylesheet(app, theme="dark_cyan.xml", invert_secondary=False)

    window.show()
    sys.exit(app.exec())
