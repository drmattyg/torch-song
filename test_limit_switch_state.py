import curses

import yaml

from torch_song.hardware import DebounceLimitSwitch
from torch_song.hardware import MCPInput

EDGE_ID = 1


def get_io(config):
    io = dict()
    mcps = dict()
    for m in config['io']['mcp23017']:
        mcp = MCPInput(m['i2c_address'], m['bits'])
        mcps[m['id']] = mcp
    io['mcp23017'] = mcps


def main(scr):
    try:
        stream = open('conf/default.yml', 'r')
        config = yaml.load(stream)
        io = get_io(config)
        beg_mcp_id = config['subsystems']['limit_switches'][EDGE_ID - 1]['beg_mcp_id']
        beg_mcp_io = config['subsystems']['limit_switches'][EDGE_ID - 1]['beg_mcp_io']
        end_mcp_id = config['subsystems']['limit_switches'][EDGE_ID - 1]['end_mcp_id']
        end_mcp_io = config['subsystems']['limit_switches'][EDGE_ID - 1]['end_mcp_io']
        ls0 = DebounceLimitSwitch(io['mcp23017'][beg_mcp_id], beg_mcp_io)
        ls1 = DebounceLimitSwitch(io['mcp23017'][end_mcp_id], end_mcp_io)
        ls01_count = 0
        ls02_count = 0
        while True:
            scr.addstr(1, 0, "LS01: {}".format(ls01_count))
            scr.addstr(2, 0, "LS02: {}".format(ls02_count))
            if ls0.get_state() is True:
                ls01_count += 1
            if ls1.get_state() is True:
                ls02_count += 1
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    curses.wrapper(main)
