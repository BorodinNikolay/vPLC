import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6 import uic
from UI import ui_vPLC
from Hardware import Mirage
from qt_material import apply_stylesheet


class Loop(QThread):
    ret = pyqtSignal(str)
    intt = pyqtSignal(int)
    def __init__(self):
        super(Loop, self).__init__()

    def run(self):
        self.AI = Mirage.MirageNAI("192.168.8.192")
        while True:
            self.result = self.AI.getValue(3)
            # print(self.result)
            self.ret.emit(f"{ float('{:.1f}'.format((self.result-4000)/160)) }%")
            self.intt.emit(int((self.result-4000)/160))


class LoopDI(QThread):
    ret = pyqtSignal(bool)
    def __init__(self):
        super(LoopDI, self).__init__()

    def run(self):
        self.DI = Mirage.MirageNAODI("192.168.8.191")
        while True:
            self.result = self.DI.getValueDI(1)
            self.ret.emit(self.result)





class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui_vPLC.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("vPLC")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon('Graphics/ico.png'))
        self.statusBar()


        self.TestThread = Loop()
        self.TestThread.start()
        self.TestThread.ret.connect(self.on_change, Qt.ConnectionType.QueuedConnection)
        self.TestThread.intt.connect(self.on_change2, Qt.ConnectionType.QueuedConnection)

        self.DIThreat = LoopDI()
        self.DIThreat.start()
        self.DIThreat.ret.connect(self.on_change3, Qt.ConnectionType.QueuedConnection)



    def on_change(self, text):
        self.ui.label.setText(text)

    def on_change2(self, intt):
        self.ui.progressBar.setValue(intt)

    def on_change3(self, result):
        if result:
            self.ui.label_2.setText("FALSE")
        else:
            self.ui.label_2.setText("TRUE")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    apply_stylesheet(app, theme="dark_pink.xml", invert_secondary=False)

    window.show()
    sys.exit(app.exec())
