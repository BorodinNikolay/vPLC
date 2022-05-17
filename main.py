import sys
import time
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

        self.NAI = Mirage.MirageNAI(host="192.168.8.192", Ch0=DB["AI0_AO0"], Ch1=DB["AI1_AO1"], Ch3=DB["AI2_T_mA"], Ch2=DB["AI3_NPSI"])
        self.NAI.start()
        self.NAI.signal.connect(self.refreshScreenData)

        self.NDI = Mirage.MirageNDI(host="192.168.8.195", Ch0=DB["220DI0_220V"], Ch1=DB["220DI1_2KeyLeft"], Ch2=DB["220DI2_2KeyRight"])
        self.NDI.start()
        self.NDI.signal.connect(self.refreshScreenData)


    def refreshScreenData(self):
        self.ui.label.setText(str(float('{:.1f}'.format((DB["AI2_T_mA"].getValue()-4000)/160))) + " %")
        self.ui.label_2.setText(str(float('{:.1f}'.format((((DB["AI3_NPSI"].getValue()-4000)/160))-50))) + " °C")
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






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    apply_stylesheet(app, theme="dark_pink.xml", invert_secondary=False)

    window.show()
    sys.exit(app.exec())
