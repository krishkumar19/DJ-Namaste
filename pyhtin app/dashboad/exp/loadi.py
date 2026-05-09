import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QSplashScreen, QDialog
import sys
from main import DashWindow

from yesyes import Ui_Form


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        loadUi("splash.ui", self)

    # self.setWindowFlags(Qt.FramelessWindowHint)

    def progress(self):
        for i in range(101):
            time.sleep(0.1)
            self.progressBar.setValue(i)


class MainWindow(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        loadUi("yesyes.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.pushButton.clicked.connect(self.goto)

    def goto(self):
        gotodash = DashWindow()
        widget.addWidget(gotodash)
        widget.setCurrentIndex(widget.currentIndex()+1)


#class DashWindow(QDialog):
  #  def __init__(self):
  #      super(QDialog, self).__init__()
   #     loadUi("krish.ui", self)
        # Remove default title bar
        #self.setWindowFlags(Qt.FramelessWindowHint)  # | Qt.WindowStaysOnTopHint -> put windows on top
        #self.setMaximumSize(1080, 720)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    splash.progress()
    MainWindow1 = DashWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(MainWindow1)
    widget = MainWindow()
    widget.show()
    splash.finish(widget)
    app.exec_()
