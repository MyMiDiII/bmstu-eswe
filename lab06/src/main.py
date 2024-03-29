import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from gui.mainwindow import Ui_MainWindow

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size' : 16, 'lines.linewidth' : 2})

from cocomo.constants import *
from cocomo.cocomo import *
from study.study import *


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

        self.ui.sbSize.valueChanged.connect(self.updateSize)

        self.__init_drivers_comboxes()
        self.__init_mode_comboxes()
        self.__init_results()

        self.ui.dsbEffortBase.valueChanged.connect(self.updateTables)
        self.ui.btnStudy.clicked.connect(self.runStudy)

        self.ui.twStages.horizontalHeader(
                ).setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.twStages.horizontalHeader(
                ).setSectionResizeMode(0,
                                       QHeaderView.ResizeMode.ResizeToContents)
        self.ui.twStages.verticalHeader(
                ).setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.ui.twActivities.horizontalHeader(
                ).setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.twActivities.horizontalHeader(
                ).setSectionResizeMode(2,
                                       QHeaderView.ResizeMode.ResizeToContents)
        self.ui.twActivities.verticalHeader(
                ).setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.ui.btnEmployees.clicked.connect(self.buildChart)

    def buildChart(self):

        def addlabels(months, empls):
            for m, e in zip(months, empls):
                plt.text(m, e, e)

        employees, _, times = self.cocomo.get_employees()

        months = []
        numbers = []
        for e, t in zip(employees, times):
            prev = len(months)
            duration = int(round(t))

            months.extend([i + prev + 1 for i in range(duration)])
            numbers.extend([e for i in range(duration)])

        plt.bar(months, numbers)
        plt.xlabel("Месяц")
        plt.xticks(months)
        plt.ylabel("Число привлеченных сотрудников")
        addlabels(months, numbers)
        plt.show()


    def updateTables(self):
        results = self.cocomo.get_results()
        effort_base = results["effort_base"]
        time_base = results["time_base"]
        effort_total = results["effort_total"]

        table = self.ui.twStages
        efforts = []
        for row in range(table.rowCount()):
            proc = int(table.item(row, 0).text())
            effort = effort_base * proc / 100
            item = QTableWidgetItem("{:.2f}".format(effort))
            table.setItem(row, 1, item)
            efforts.append(effort)

            proc = int(table.item(row, 2).text())
            item = QTableWidgetItem("{:.2f}".format(time_base * proc / 100))
            table.setItem(row, 3, item)

        analyst     = 160000
        manager     = 140000
        architect   = 250000
        teamlead    = 220000
        developer   = 165000
        qa_engineer = 150000

        price = (analyst + manager + architect + teamlead + developer +
                 qa_engineer) / 6 / 1000

        table = self.ui.twActivities
        for row in range(table.rowCount()):
            proc = int(table.item(row, 0).text())
            effort = effort_total * proc / 100
            item = QTableWidgetItem("{:.2f}".format(effort))
            table.setItem(row, 1, item)

            item = QTableWidgetItem("{:.2f}".format(effort * price))
            table.setItem(row, 2, item)


        #stages_prices = {
        #        "plan" : ,
        #        "design-high" : ,
        #        "design-low" :,
        #        "code-test" : ,
        #        "integration-test":
        #        }

    def updateSize(self):
        self.cocomo.set_size(self.ui.sbSize.value())

    def __init_results(self):
        self.ui.dsbC1.valueChanged.connect(self.updateEffortBase)
        self.ui.dsbP1.valueChanged.connect(self.updateEffortBase)
        self.ui.sbSize.valueChanged.connect(self.updateEffortBase)
        self.ui.dsbEAF.valueChanged.connect(self.updateEffortBase)

        self.ui.dsbC2.valueChanged.connect(self.updateTimeBase)
        self.ui.dsbP2.valueChanged.connect(self.updateTimeBase)

        self.ui.dsbEffortBase.valueChanged.connect(self.updateAll)

    def updateEffortBase(self):
        effort_base = self.cocomo.get_results()["effort_base"]
        self.ui.dsbEffortBase.setValue(effort_base)

    def updateTimeBase(self):
        time_base = self.cocomo.get_results()["time_base"]
        self.ui.dsbTimeBase.setValue(time_base)

    def updateAll(self):
        results = self.cocomo.get_results()

        effort_plan = results["effort_plan"]
        effort_total = results["effort_total"]

        time_base  = results["time_base"]
        time_plan  = results["time_plan"]
        time_total = results["time_total"]

        self.ui.dsbEffortPlan.setValue(effort_plan)
        self.ui.dsbEffortTotal.setValue(effort_total)
        self.ui.dsbTimeBase.setValue(time_base)
        self.ui.dsbTimePlan.setValue(time_plan)
        self.ui.dsbTimeTotal.setValue(time_total)

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

    def runStudy(self):
        StudySWCocomo(250, CocomoModes.SEMIDETACHED).run(Level.NOMINAL)
        StudySWCocomo(250, CocomoModes.SEMIDETACHED).run(Level.HIGH)
        StudySWCocomo(250, CocomoModes.SEMIDETACHED).run(Level.VERY_HIGH)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
