import sys

from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def main():
    from PyQt5.QtWidgets import QStyleFactory
    print(QStyleFactory.keys())
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
