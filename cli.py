#!/usr/bin/python

import sys
from os import path
import cmd
import yaml

#sys.path.append(path.dirname(path.abspath(__file__)) + '/test')
#sys.path.append(path.dirname(path.abspath(__file__)) + '/torch_song')

from test.test_mcp import mcp_cli
from test.test_pca9685 import pca9685_cli
from test.test_motor_driver import motor_driver_cli
from test.test_igniter import igniter_cli
from test.test_valve import valve_cli

stream = open('conf/default.yml', 'r')
config = yaml.load(stream)

class test_cli(cmd.Cmd):
    def __init__(self):
        self.intro = 'Torch Song CLI'
        self.prompt = 'Torch > '
        self.doc_header='Torch Song Cli (type help):'
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
    def do_mcp23017(self, args):
        mcp_cli(config).cmdloop()
    def help_mcp23017(self):
        print('MCP23017 test interface')
    def do_pca9685(self, args):
        pca9685_cli(config).cmdloop()
    def help_pca9685(self):
        print('PCA9685 test interface')
    def do_igniter(self, args):
        igniter_cli(config).cmdloop()
    def help_igniter(self):
        print('Igniter test interface')
    def do_valve(self, args):
        valve_cli(config).cmdloop()
    def help_valve(self):
        print('Valve test interface')
    def do_motor_driver(self, args):
        motor_driver_cli(config).cmdloop()
    def help_motor_driver(self):
        print('Motor Driver test interface')

if __name__ == '__main__':
    cli = test_cli()
    cli.cmdloop()


