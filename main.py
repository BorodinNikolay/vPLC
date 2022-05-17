import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
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


        self.NAI = Mirage.MirageNAI(host="192.168.8.192", Ch3=DB["Krutilka"], Ch2=DB["TempInside"])
        self.NAI.start()

        # self.Refresh = Refresh(refreshTime=0.1)
        # self.Refresh.start()

        # self.Refresh.refreshSignal.connect(self.refreshScreenData)
        self.NAI.signal.connect(self.refreshScreenData)

    def refreshScreenData(self):
        self.ui.label.setText(str(float('{:.1f}'.format((DB["Krutilka"].getValue()-4000)/160))) + " %")
        self.ui.label_2.setText(str(DB["TempInside"].getValue()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    apply_stylesheet(app, theme="dark_pink.xml", invert_secondary=False)

    window.show()
    sys.exit(app.exec())
