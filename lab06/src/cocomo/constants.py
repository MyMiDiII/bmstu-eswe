from enum import Enum, auto
from dataclasses import dataclass

@dataclass
class ModeCoeffs:
    c1: float
    p1: float
    c2: float
    p2: float

class CocomoModes(Enum):
    ORGANIC      = 0
    SEMIDETACHED = 1
    EMBEDDED     = 2

MODES = {
    CocomoModes.ORGANIC      : ModeCoeffs(3.2, 1.05, 2.5, 0.38),
    CocomoModes.SEMIDETACHED : ModeCoeffs(3.0, 1.12, 2.5, 0.35),
    CocomoModes.EMBEDDED     : ModeCoeffs(2.8, 1.20, 2.5, 0.32),
}

class Level(Enum):
    VERY_LOW = 0
    LOW = 1
    NOMINAL = 2
    HIGH = 3
    VERY_HIGH = 4

class Driver(Enum):
    RELY = 0
    DATA = 1
    CPLX = 2

    TIME = 3
    STOR = 4
    VIRT = 5
    TURN = 6

    MODP = 7
    TOOL = 8
    SCED = 9

    ACAP = 10
    AEXP = 11
    PCAP = 12
    VEXP = 13
    LEXP = 14


class DriversCoeffs:
    coeffs_table = [
        [0.75, 0.86, 1.00, 1.15, 1.40],
        [None, 0.94, 1.00, 1.08, 1.16],
        [0.70, 0.85, 1.00, 1.15, 1.30],

        [None, None, 1.00, 1.11, 1.50],
        [None, None, 1.00, 1.06, 1.21],
        [None, 0.87, 1.00, 1.15, 1.30],
        [None, 0.87, 1.00, 1.07, 1.15],

        [1.24, 1.10, 1.00, 0.91, 0.82],
        [1.24, 1.10, 1.00, 0.91, 0.82],
        [1.23, 1.08, 1.00, 1.04, 1.10],

        [1.46, 1.19, 1.00, 0.86, 0.71],
        [1.29, 1.15, 1.00, 0.91, 0.82],
        [1.42, 1.17, 1.00, 0.86, 0.70],
        [1.21, 1.10, 1.00, 0.90, None],
        [1.14, 1.07, 1.00, 0.95, None]
    ]

    @classmethod
    def get_coef(cls, driver: Driver, level: Level = Level.NOMINAL):
        return cls.coeffs_table[driver.value][level.value]

