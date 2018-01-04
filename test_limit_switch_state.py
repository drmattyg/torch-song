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
    return io


def main(scr):
    try:
        # stream = open('conf/default.yml', 'r')
        # config = yaml.load(stream)
        # io = get_io(config)
        # beg_mcp_id = config['subsystems']['limit_switches'][EDGE_ID - 1]['beg_mcp_id']
        # beg_mcp_io = config['subsystems']['limit_switches'][EDGE_ID - 1]['beg_mcp_io']
        # end_mcp_id = config['subsystems']['limit_switches'][EDGE_ID - 1]['end_mcp_id']
        # end_mcp_io = config['subsystems']['limit_switches'][EDGE_ID - 1]['end_mcp_io']
        mcp = MCPInput(0x22, 16)
        ls1 = DebounceLimitSwitch(mcp, 0)
        ls2 = DebounceLimitSwitch(mcp, 1)
        ls1_count = 0
        ls2_count = 0
        s1 = ls1.get_state()
        s2 = ls2.get_state()
        while True:
            scr.addstr(1, 0, "LS01: {} ({})".format(s1, ls1_count))
            scr.addstr(2, 0, "LS02: {} ({})".format(s2, ls2_count))
            if s1 is True:
                ls1_count += 1
            if s2 is True:
                ls2_count += 1
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    curses.wrapper(main)
