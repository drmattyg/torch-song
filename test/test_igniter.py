import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import yaml

from torch_song.igniter import Igniter

class igniter_cli(cmd.Cmd):
    def __init__(self, config):
        self.intro = 'Igniter CLI'
        self.prompt = 'Igniters > '
        self.doc_header='Igniter Cli (type help):'

        self.igniters = {}
        for v in config['subsystems']['igniters']:
            igniter = Igniter(v['gpio'])
            self.igniters[v['id']] = igniter

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
        self.igniters[which].set_state(state)
        state = self.igniters[which].get_state()
        print('igniter%s is now %s' % (which, 'CLOSED' if state == Igniter.ON else 'OPEN'))
    def help_set(self):
        print('to close igniter 1, usage: set 1 1')
    def do_read(self, args):
        for id, igniter in self.igniters.iteritems():
            state = igniter.get_state()
            print('igniter%s is %s' % (id, 'CLOSED' if state == Igniter.ON else 'OPEN'))
    def help_read(self):
        print('read all igniters')

if __name__ == '__main__':
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    cli = igniter_cli(config)
    cli.cmdloop()

