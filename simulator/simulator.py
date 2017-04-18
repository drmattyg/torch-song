import threading
import time


class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    MAGENTA = '\033[45m'
    BG_YELLOW = '\033[43m'
    UP = "\033[1A"
    DOWN = "\033[1B"
    BACK = "\033[1D"
    OFF = "\033[0m"


def color_string(color, s, bool):
    if not bool:
        return s
    return color + s + bcolors.OFF


def up_string(s):
    return bcolors.BACK + bcolors.UP + s + bcolors.DOWN


class SimEdge:
    # a software simulated edge
    SLEEP_TIME = 50.0
    STR_LEN = 10
    REPR = "{id} {valve} {igniter} {ls0}:{left}{shuttle}{right}:{ls1}"

    def __init__(self, id, default_calibration_time=4000):
        self.id = id
        self.calibration_time = default_calibration_time
        self.position = 0
        self.motor_speed = 0
        self.motor_direction = 0
        self.valve = False
        self.igniter = False
        self.limit_switches = [False, False]
        self._runner_thread = threading.Thread(target=self._runner)

    def _runner(self):
        if self.position <= 0:
            self.position = 0
            self.limit_switches[0] = True
        if self.position >= 1:
            self.position = 1
            self.limit_switches[1] = True
        time.sleep(SimEdge.SLEEP_TIME / 1000.0)
        self.position += self.direction * \
                         (SimEdge.SLEEP_TIME / self.calibration_time) * self.speed / 100.0

    def __str__(self):
        pos = int(SimEdge.STR_LEN * self.position)
        left_pad = "_" * pos
        right_pad = "_" * (9 - pos)
        ls0 = color_string(bcolors.GREEN, 'L', self.limit_switches[0])
        ls1 = color_string(bcolors.GREEN, 'R', self.limit_switches[1])
        valve = color_string(bcolors.GREEN, 'V', self.valve)
        igniter = color_string(bcolors.RED, 'I', self.valve)
        if self.igniter:
            shuttle = color_string(bcolors.MAGENTA, "=", True)
        elif self.valve:
            shuttle = "=" + up_string(bcolors.BG_YELLOW + bcolors.RED + "*" + bcolors.OFF)
        else:
            shuttle = color_string(bcolors.BLUE, "=", True)
        return SimEdge.REPR.format(id=self.id, valve=valve, igniter=igniter, ls0=ls0, ls1=ls1,
                                   left=left_pad,
                                   right=right_pad, shuttle=shuttle)


if __name__ == "__main__":
    se = SimEdge(0)
    se.position = 0.91
    se.valve = 0
    print("\n")
    print(se)
