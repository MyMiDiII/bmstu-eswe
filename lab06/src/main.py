import sys

from PyQt5 import QtWidgets
from gui.mainwindow import Ui_MainWindow

from cocomo.constants import *
from cocomo.cocomo import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.cocomo = Cocomo(40, CocomoModes.ORGANIC)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.drivers_comboxes = [
                self.ui.cbRELY,
                self.ui.cbDATA,
                self.ui.cbCPLX,

                self.ui.cbTIME,
                self.ui.cbSTOR,
                self.ui.cbVIRT,
                self.ui.cbTURN,

                self.ui.cbMODP,
                self.ui.cbTOOL,
                self.ui.cbSCED,

                self.ui.cbACAP,
                self.ui.cbAEXP,
                self.ui.cbPCAP,
                self.ui.cbVEXP,
                self.ui.cbLEXP
                ]

        self.drivers_spinboxes = [
                self.ui.dsbRELY,
                self.ui.dsbDATA,
                self.ui.dsbCPLX,

                self.ui.dsbTIME,
                self.ui.dsbSTOR,
                self.ui.dsbVIRT,
                self.ui.dsbTURN,

                self.ui.dsbMODP,
                self.ui.dsbTOOL,
                self.ui.dsbSCED,

                self.ui.dsbACAP,
                self.ui.dsbAEXP,
                self.ui.dsbPCAP,
                self.ui.dsbVEXP,
                self.ui.dsbLEXP
                ]

        self.__init_drivers_comboxes()


    def __init_drivers_comboxes(self):
        baseText = [
                "Очень низкий",
                "Низкий",
                "Номинальный",
                "Высокий",
                "Очень высокий",
                ]
        cbItems = [
                [baseText,      2],
                [baseText[1:],  1],
                [baseText,      2],

                [baseText[2:],  0],
                [baseText[2:],  0],
                [baseText[1:],  1],
                [baseText[1:],  1],

                [baseText,      2],
                [baseText,      2],
                [baseText,      2],

                [baseText,      2],
                [baseText,      2],
                [baseText,      2],
                [baseText[:-1], 2],
                [baseText[:-1], 2]
                ]


        for i, combox in enumerate(self.drivers_comboxes):
            combox.addItems(cbItems[i][0])
            f = lambda y, x=i: self.syncDriverSB(x,
                       self.drivers_comboxes[x],
                       self.drivers_spinboxes[x],
                       Driver(x),
                       cbItems[x][1])
            combox.currentIndexChanged.connect(f)
            combox.setCurrentIndex(cbItems[i][1])


    def syncDriverSB(self, x, combox, spinbox, driver, nominal):
        index = combox.currentIndex()

        self.cocomo.set_driver(driver, Level(2 - nominal + index))
        value = self.cocomo.get_driver(driver)

        spinbox.setValue(value)
        self.ui.dsbEAF.setValue(self.cocomo.get_results()["eaf"])


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
