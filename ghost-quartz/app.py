from PyQt5 import (QtWidgets, QtGui, QtCore)
from main_window import MainWindow
import logging
import faulthandler

# Logging setup
logging.basicConfig(level=logging.DEBUG)


def app():
    # Trace debugger
    faulthandler.enable()
    ghost = QtWidgets.QApplication([])
    window = MainWindow()
    print(window.size().height())
    ghost.exec_()


if __name__ == "__main__":
    app()
