import threading
import time
import curses
from enum import Enum


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
        self.motor_direction = 1
        self.valve = False
        self.igniter = False
        self.limit_switches = [False, False]
        self._run_thread = threading.Event()
        self._run_thread.set()
        self._runner_thread = threading.Thread(target=self._runner)
        self.x_offset = 0
        # self._runner_thread.start()

    def _runner(self):
        while self._run_thread.is_set():
            self.position += self.motor_direction * \
                             (SimEdge.SLEEP_TIME / self.calibration_time) * self.motor_speed / 100.0

            if self.position <= 0:
                self.position = 0
                self.limit_switches[0] = True
            else:
                self.limit_switches[0] = False
            if self.position >= 1:
                self.position = 1
                self.limit_switches[1] = True
            else:
                self.limit_switches[1] = False
            if self.position > 1:
                self.position = 1
            if self.position < 0:
                self.position = 0
            time.sleep(SimEdge.SLEEP_TIME / 1000.0)

    def start(self):
        self._runner_thread.start()

    def __str__(self):
        pos = min([int(SimEdge.STR_LEN * self.position), 9])
        left_pad = "_" * pos
        right_pad = "_" * (9 - pos)
        ls0 = color_string(bcolors.GREEN, 'L', self.limit_switches[0])
        ls1 = color_string(bcolors.GREEN, 'R', self.limit_switches[1])
        valve = color_string(bcolors.GREEN, 'V', self.valve)
        igniter = color_string(bcolors.RED, 'I', self.igniter)
        if self.igniter:
            shuttle = color_string(bcolors.MAGENTA, "=", True)
        elif self.valve:
            shuttle = "=" + up_string(bcolors.BG_YELLOW + bcolors.RED + "*" + bcolors.OFF)
        else:
            shuttle = color_string(bcolors.BLUE, "=", True)
        return SimEdge.REPR.format(id=self.id, valve=valve, igniter=igniter, ls0=ls0, ls1=ls1,
                                   left=left_pad,
                                   right=right_pad, shuttle=shuttle)

    def draw_str(self, scr, x_offset, y_offset):
        SimEdge.draw_str.x_offset = x_offset  # weird python scoping rules

        def append_str(s, color=SimEdge.Colors.OFF, b=False):
            scr.addstr(y_offset, self.x_offset, s, curses.color_pair(color.value * b))
            self.x_offset += len(s)

        pos = min([int(SimEdge.STR_LEN * self.position), 9])
        left_pad = "_" * pos
        right_pad = "_" * (9 - pos)
        append_str(str(self.id) + " ")
        append_str("V ", color=SimEdge.Colors.VALVE, b=self.valve)

        append_str("I ", color=SimEdge.Colors.IGNITER, b=self.igniter)
        append_str("L", color=SimEdge.Colors.LIMIT_SWITCH, b=self.limit_switches[0])
        append_str(left_pad)
        append_str("=", color=SimEdge.Colors.FLAME, b=self.valve)
        append_str(right_pad)
        append_str("R", color=SimEdge.Colors.LIMIT_SWITCH, b=self.limit_switches[1])
        if self.valve:
            scr.addstr(y_offset - 1, pos + 7, "&", curses.color_pair(SimEdge.Colors.FIRE.value))
            scr.clrtoeol()
        scr.clrtoeol()
        self.x_offset = 0

    def kill(self):
        self._run_thread.clear()
        self._runner_thread.join()

    class Colors(Enum):
        ON = 1
        OFF = 0
        LIMIT_SWITCH = 2
        VALVE = 3
        IGNITER = 4
        FLAME = 5
        FIRE = 6

    @staticmethod
    def initialize_colors():
        curses.init_pair(SimEdge.Colors.ON.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(SimEdge.Colors.LIMIT_SWITCH.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(SimEdge.Colors.VALVE.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(SimEdge.Colors.IGNITER.value, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(SimEdge.Colors.FLAME.value, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(SimEdge.Colors.FIRE.value, curses.COLOR_RED, curses.COLOR_BLACK)


class SimTorchSong:
    def __init__(self, scr):
        self.edges = [SimEdge(id) for id in range(9)]
        self.scr = scr
        SimEdge.initialize_colors()

    def render(self):
        self.scr.clear()
        for i, edge in enumerate(self.edges):
            y = (i + 1) * 3
            edge.draw_str(self.scr, 3, y)

    def kill(self):
        for edge in self.edges:
            edge.kill()

    def __del__(self):
        self.kill()


def main(scr):
    scr.nodelay(1)
    SimEdge.initialize_colors()
    se = SimEdge(0)
    se.motor_speed = 100
    se.start()
    try:
        while True:
            se.draw_str(scr, 3, 3)
            time.sleep(0.1)
            if se.limit_switches[0] or se.limit_switches[1]:
                se.motor_direction *= -1
                se.valve = 1 - se.valve
            s = scr.getstr()
            if s == "q":
                break
        se.kill()
    except KeyboardInterrupt:
        se.kill()


if __name__ == "__main__":
    curses.wrapper(main)