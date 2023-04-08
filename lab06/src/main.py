import sys

from PyQt5 import QtWidgets
from gui.mainwindow import Ui_MainWindow

from cocomo.constants import *
from cocomo.cocomo import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cocomo = Cocomo(self.ui.sbSize.value(), CocomoModes.ORGANIC)

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
        self.__init_mode_comboxes()
        self.__init_results()

        self.ui.sbSize.valueChanged.connect(self.updateSize)

    def updateSize(self):
        self.cocomo.set_size(self.ui.sbSize.value())

    def __init_results(self):
        self.ui.dsbC1.valueChanged.connect(self.updateEffort)
        self.ui.dsbP1.valueChanged.connect(self.updateEffort)
        self.ui.sbSize.valueChanged.connect(self.updateEffort)
        self.ui.dsbEAF.valueChanged.connect(self.updateEffort)


    def updateEffort(self):
        effort_base = self.cocomo.get_results()["effort_base"]
        self.ui.dsbEffortBase.setValue(effort_base)


    def __init_mode_comboxes(self):
        modes = [
                "Обычный",
                "Промежуточный",
                "Встроенный"
                ]

        self.ui.cbMode.addItems(modes)
        self.ui.cbMode.currentIndexChanged.connect(self.changeCocomoCoefs)
        self.changeCocomoCoefs()


    def changeCocomoCoefs(self):
        modeIndex = self.ui.cbMode.currentIndex()
        self.cocomo.set_mode(CocomoModes(modeIndex))

        mode = self.cocomo.get_results()["mode"]

        self.ui.dsbC1.setValue(mode.c1)
        self.ui.dsbP1.setValue(mode.p1)
        self.ui.dsbC2.setValue(mode.c2)
        self.ui.dsbP2.setValue(mode.p2)


    def __init_drivers_comboxes(self):
        baseText = [
                "Очень низкий",
                "Низкий",
                "Номинальный",
                "Высокий",
                "Очень высокий"
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
            f = lambda y, x=i: self.syncDriverSB(
                       self.drivers_comboxes[x],
                       self.drivers_spinboxes[x],
                       Driver(x),
                       cbItems[x][1])
            combox.currentIndexChanged.connect(f)
            combox.setCurrentIndex(cbItems[i][1])
            f(0, i)


    def syncDriverSB(self, combox, spinbox, driver, nominal):
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
