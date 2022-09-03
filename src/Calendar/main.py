from PyQt5 import QtWidgets

from mainwindow import Ui_MainWindow
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())
