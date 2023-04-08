import math

from cocomo.constants import *

class Cocomo:
    def __init__(self, kloc, mode):
        self.drivers = {
            Driver.RELY : DriversCoeffs.get_coef(Driver.RELY),
            Driver.DATA : DriversCoeffs.get_coef(Driver.DATA),
            Driver.CPLX : DriversCoeffs.get_coef(Driver.CPLX),

            Driver.TIME : DriversCoeffs.get_coef(Driver.TIME),
            Driver.STOR : DriversCoeffs.get_coef(Driver.STOR),
            Driver.VIRT : DriversCoeffs.get_coef(Driver.VIRT),
            Driver.TURN : DriversCoeffs.get_coef(Driver.TURN),

            Driver.MODP : DriversCoeffs.get_coef(Driver.MODP),
            Driver.TOOL : DriversCoeffs.get_coef(Driver.TOOL),
            Driver.SCED : DriversCoeffs.get_coef(Driver.SCED),

            Driver.ACAP : DriversCoeffs.get_coef(Driver.ACAP),
            Driver.AEXP : DriversCoeffs.get_coef(Driver.AEXP),
            Driver.PCAP : DriversCoeffs.get_coef(Driver.PCAP),
            Driver.VEXP : DriversCoeffs.get_coef(Driver.VEXP),
            Driver.LEXP : DriversCoeffs.get_coef(Driver.LEXP)
        }

        self.size = kloc
        self.mode = MODES[mode]

    @property
    def eaf(self):
        return math.prod(self.drivers.values())

    @property
    def effort_base(self):
        return self.mode.c1 * self.eaf * self.size ** self.mode.p1

    @property
    def time_base(self):
        return self.mode.c2 * self.effort_base ** self.mode.p2

    def get_results(self):
        return {
                "eaf" : self.eaf,
                "mode" : self.mode,
                "effort_base" : self.effort_base,
                "time_base" : self.time_base
                }

    def set_drivers(self, drivers: dict):
        for key, values in drivers.items():
            self.drivers[key] = value

    def set_driver(self, driver, level):
        self.drivers[driver] = DriversCoeffs.get_coef(driver, level)

    def get_driver(self, driver):
        return self.drivers[driver]

    def set_mode(self, mode):
        self.mode = MODES[mode]
