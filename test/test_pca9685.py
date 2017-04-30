import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import yaml

from torch_song.pca9685 import PCA9685

class pca9685_cli(cmd.Cmd):
    def __init__(self, config):
        self.intro = 'PCA9685 CLI'
        self.prompt = 'PCA9685 > '
        self.doc_header = 'PCA9685 Cli (type help):'

        self.pca9685 = PCA9685();

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
    def do_setduty(self, args):
        channel = int(args.split()[0])
        duty = int(args.split()[1])
        self.pca9685.set_duty(channel, duty)

if __name__ == '__main__':
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    cli = pca9685_cli(config)
    cli.cmdloop()

