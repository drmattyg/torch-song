import sys
from os import path
import cmd
import yaml

sys.path.append(path.dirname(path.abspath(__file__)) + '/test')

from test_relay_cli import relay_cli
from test_mcp_cli import mcp_cli

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
    def do_relays(self, args):
        relay_cli(config).cmdloop()
    def help_relays(self):
        print('Relay test interface')
    def do_mcp23017(self, args):
        mcp_cli(config).cmdloop()
    def help_mcp23017(self):
        print('MCP23017 test interface')

if __name__ == '__main__':
    cli = test_cli()
    cli.cmdloop()


