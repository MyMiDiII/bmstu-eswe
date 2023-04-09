import matplotlib.pyplot as plt

from cocomo.cocomo import *

class StudySWCocomo:
    def __init__(self, size, mode):
        self.size = size
        self.mode = mode

        self.cocomo = Cocomo(size, mode)

        self.levels = [
                "Очень низкий",
                "Низкий",
                "Номинальный",
                "Высокий",
                "Очень высокий"
                ]

        self.drivers = [
                "RELY",
                "DATA",
                "CPLX"
                ]


    def study_driver(self, driver, levels):
        efforts = []
        times = []
        for level in levels:
            self.cocomo.set_driver(driver, level)

            result = self.cocomo.get_results()
            efforts.append(result["effort_base"])
            times.append(result["time_base"])

            self.cocomo.set_driver(driver, Level.NOMINAL)

        return efforts, times

    def run(self, sced_level):
        self.cocomo.set_driver(Driver.SCED, sced_level)

        levels = [Level(i) for i in range(5)]
        drivers = [
                [Driver.RELY, levels],
                [Driver.DATA, levels[1:]],
                [Driver.CPLX, levels],
                ]

        effort_results = []
        times_results = []
        for driver, level in drivers:
            efforts, times = self.study_driver(driver, level)
            effort_results.append(efforts)
            times_results.append(times)

        self.cocomo.set_driver(Driver.SCED, Level.NOMINAL)

        sced_levels = {
                Level.NOMINAL : "номинальный",
                Level.HIGH : "высокий",
                Level.VERY_HIGH : "очень высокий"
                }

        self.graph(effort_results, times_results, sced_levels[sced_level])


    def graph(self, efforts, times, title):
        plt.figure()
        plt.rcParams.update({'font.size' : 16, 'lines.linewidth' : 2})

        self.graph_subplot(1, 2, 1, efforts, "Трудозатраты")
        self.graph_subplot(1, 2, 2, times, "Время")

        plt.suptitle(f"Уровень SCED: {title}")
        plt.show()


    def graph_subplot(self, rows, columns, num, values, ylabel):
        plt.subplot(rows, columns, num)

        for value, driver in zip(values, self.drivers):
            tmp_levels = self.levels[len(self.levels) - len(value):]
            plt.plot(tmp_levels, value, label=driver)

        plt.xlabel("Уровень")
        plt.ylabel(ylabel)
        plt.grid()
        plt.legend()
