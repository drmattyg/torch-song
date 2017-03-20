import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import yaml

from relay import Relay

class relay_cli(cmd.Cmd):
    def __init__(self, config):
        self.intro = 'Relay CLI'
        self.prompt = 'Relays > '
        self.doc_header='Relay Cli (type help):'

        self.relays = {}
        for r in config['io']['relays']:
            relay = Relay(r['gpio_pin'])
            self.relays[r['id']] = relay

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
        self.relays[which].set_state(state)
        state = self.relays[which].get_state()
        print('relay%s is now %s' % (which, 'CLOSED' if state == Relay.CLOSED else 'OPEN'))
    def help_set(self):
        print('to close relay 1, usage: set 1 1')
    def do_read(self, args):
        for id, relay in self.relays.iteritems():
            state = relay.get_state()
            print('relay%s is %s' % (id, 'CLOSED' if state == Relay.CLOSED else 'OPEN'))
    def help_read(self):
        print('read all relays')

if __name__ == '__main__':
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    cli = relay_cli(config)
    cli.cmdloop()

