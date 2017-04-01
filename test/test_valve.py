import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import yaml

from valve import Valve

class valve_cli(cmd.Cmd):
    def __init__(self, config):
        self.intro = 'Valve CLI'
        self.prompt = 'Valves > '
        self.doc_header='Valve Cli (type help):'

        self.valves = {}
        for v in config['subsystems']['valves']:
            valve = Valve(v['gpio_pin'])
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
    def do_set(self, args):
        which = int(args.split()[0])
        state = int(args.split()[1])
        self.valves[which].set_state(state)
        state = self.valves[which].get_state()
        print('valve%s is now %s' % (which, 'CLOSED' if state == Valve.CLOSED else 'OPEN'))
    def help_set(self):
        print('to close valve 1, usage: set 1 1')
    def do_read(self, args):
        for id, valve in self.valves.iteritems():
            state = valve.get_state()
            print('valve%s is %s' % (id, 'CLOSED' if state == Valve.CLOSED else 'OPEN'))
    def help_read(self):
        print('read all valves')

if __name__ == '__main__':
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    cli = valve_cli(config)
    cli.cmdloop()

