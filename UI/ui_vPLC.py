# Form implementation generated from reading ui file 'vPLC.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Tabs = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Tabs.setFont(font)
        self.Tabs.setTabShape(QtWidgets.QTabWidget.TabShape.Triangular)
        self.Tabs.setElideMode(QtCore.Qt.TextElideMode.ElideNone)
        self.Tabs.setDocumentMode(True)
        self.Tabs.setTabsClosable(False)
        self.Tabs.setTabBarAutoHide(False)
        self.Tabs.setObjectName("Tabs")
        self.Status = QtWidgets.QWidget()
        self.Status.setObjectName("Status")
        self.pushButton = QtWidgets.QPushButton(self.Status)
        self.pushButton.setGeometry(QtCore.QRect(20, 50, 171, 51))
        self.pushButton.setObjectName("pushButton")
        self.layoutWidget = QtWidgets.QWidget(self.Status)
        self.layoutWidget.setGeometry(QtCore.QRect(210, 310, 411, 161))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.Status)
        self.label_2.setGeometry(QtCore.QRect(218, 180, 401, 91))
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setWordWrap(False)
        self.label_2.setOpenExternalLinks(False)
        self.label_2.setObjectName("label_2")
        self.Tabs.addTab(self.Status, "")
        self.Communications = QtWidgets.QWidget()
        self.Communications.setObjectName("Communications")
        self.Tabs.addTab(self.Communications, "")
        self.OPC = QtWidgets.QWidget()
        self.OPC.setObjectName("OPC")
        self.Tabs.addTab(self.OPC, "")
        self.SQL = QtWidgets.QWidget()
        self.SQL.setObjectName("SQL")
        self.Tabs.addTab(self.SQL, "")
        self.DB = QtWidgets.QWidget()
        self.DB.setObjectName("DB")
        self.Tabs.addTab(self.DB, "")
        self.horizontalLayout.addWidget(self.Tabs)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "TEXT TEXT"))
        self.label_2.setText(_translate("MainWindow", "Digital Input"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Status), _translate("MainWindow", "Статус"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Communications), _translate("MainWindow", "Соединения"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.OPC), _translate("MainWindow", "OPC"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.SQL), _translate("MainWindow", "SQL"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.DB), _translate("MainWindow", "DB"))
