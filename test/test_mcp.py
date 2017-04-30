import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import yaml

from torch_song.mcp23017 import MCPInput

class mcp_cli(cmd.Cmd):
    def __init__(self, config):
        self.intro = 'MCP23017 CLI'
        self.prompt = 'MCP23017 > '
        self.doc_header = 'MCP23017 Cli (type help):'

        self.mcps = {}
        for m in config['io']['mcp23017']:
            mcp = MCPInput(m['i2c_address'], m['bits'])
            self.mcps[m['id']] = mcp

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
    def do_readall(self, args):
        for k,v in self.mcps.iteritems():
            print('mcp23017 id:%s' % k)
            for i, val in enumerate(v.update()):
                print('  %d: %d' % (i, val))
    def help_readall(self):
        print('read all MCP23017 IO')

if __name__ == '__main__':
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    cli = mcp_cli(config)
    cli.cmdloop()

