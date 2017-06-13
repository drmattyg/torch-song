import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import yaml

from time import sleep

from torch_song.edge.real_edge import RealEdge
from torch_song.hardware import PCA9685
from torch_song.hardware import MCPInput

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

        self.edge = RealEdge(4, self.io, config)

        cmd.Cmd.__init__(self)
    def emptyline(self):
        pass
    def do_end(self, args):
        do_stop(args)
        return True
    def help_end(self, args):
        print('End session')
    do_EOF = do_end
    help_EOF = help_end
    def do_quit(self, args):
        do_stop(args)
        return True
    def help_quit(self, args):
        print('Quit session')
    def do_set_motor(self, args):
        speed = int(args.split()[0])
        dir = int(args.split()[1])
        self.edge.set_motor_state(int(dir), int(speed))
    def do_set_valve(self, args):
        self.edge.set_valve_state(int(args))
        print(self.edge)
    def do_set_igniter(self, args):
        self.edge.set_igniter_state(int(args))
        print(self.edge)
    def do_get_limit_switch(self, args):
        print(self.edge.get_limit_switch_state())
    def do_state(self, args):
        print(self.edge)
    def do_stop(self, args):
        self.edge.set_motor_state(0, 0)
        self.edge.set_igniter_state(0)
        self.edge.set_valve_state(0)
        print(self.edge)
    def do_back_and_forth(self, args):
        d = int(0)
        speed = int(args) if len(args) > 0 else 60
        while True:
            print(self.edge)
            self.edge.set_motor_state(d, 60)
            if (d == 0 and self.edge.get_limit_switch_state()[1]):
                d = 1
                self.edge.set_igniter_state(1)
                sleep(3)
                self.edge.set_valve_state(1)
                self.edge.set_igniter_state(0)

            if (d == 1 and self.edge.get_limit_switch_state()[0]):
                self.edge.set_valve_state(0)
                d = 0   
            sleep(.1)


if __name__ == '__main__':
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    cli = edge_cli(config)
    cli.cmdloop()

