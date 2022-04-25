import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("vPLC")
        self.setMinimumSize(800, 600)
        # self.setWindowIcon(QIcon('Graphics/ico.png'))
        self.statusBar()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
