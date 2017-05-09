import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import yaml

from torch_song.igniter import Igniter
from torch_song.valve import Valve

class load_cli(cmd.Cmd):
    def __init__(self, config):
        self.intro = 'Load Test CLI'
        self.prompt = 'Load > '
        self.doc_header='Load Cli (type help):'

        self.igniters = {}
        for v in config['subsystems']['igniters']:
            igniter = Igniter(v['gpio'])
            self.igniters[v['id']] = igniter

        self.valves = {}
        for v in config['subsystems']['valves']:
            valve = Valve(v['gpio'])
            self.valves[v['id']] = valve

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
    def do_all_on(self, args):
        for k, v in self.igniters.iteritems():
            v.set_state(1)
        for k, v in self.valves.iteritems():
            v.set_state(1)
        print('All relays turned on')
    def do_all_off(self, args):
        for k, v in self.igniters.iteritems():
            v.set_state(0)
        for k, v in self.valves.iteritems():
            v.set_state(0)

if __name__ == '__main__':
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    cli = load_cli(config)
    cli.cmdloop()

