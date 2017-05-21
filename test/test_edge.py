import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import yaml

from torch_song.torch_song.real_edge import RealEdge
from torch_song.pca9685 import PCA9685
from torch_song.mcp23017 import MCPInput

class edge_cli(cmd.Cmd):
    def __init__(self, config):
        self.intro = 'Single Edge CLI'
        self.prompt = 'Edge > '
        self.doc_header='Edge Cli (type help):'

        self.io = {}
        self.io['pca9685']= PCA9685()
        mcps = {}
        for m in config['io']['mcp23017']:
            mcp = MCPInput(m['i2c_address'], m['bits'])
            mcps[m['id']] = mcp
        self.io['mcp23017']= mcps

        self.edge = RealEdge(1, self.io, config)

        cmd.Cmd.__init__(self)
    def emptyline(self):
        pass
    def do_end(self, args):
        return True
    def help_end(self, args):
        print('End session')
    do_EOF = do_end
    help_EOF = help_end
    def do_quit(self, args):
        return True
    def help_quit(self, args):
        print('Quit session')
    def do_set_motor(self, args):
        speed = int(args.split()[0])
        dir = int(args.split()[1])
        self.edge.set_motor_state(int(dir), int(speed))
    def do_set_valve(self, args):
        self.edge.set_valve_state(int(args))
    def do_set_igniter(self, args):
        self.edge.set_igniter_state(int(args))
    def do_get_limit_switch(self, args):
        print(self.edge.get_limit_switch_state())
    def do_state(self, args):
        print(self.edge)

if __name__ == '__main__':
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    cli = edge_cli(config)
    cli.cmdloop()

