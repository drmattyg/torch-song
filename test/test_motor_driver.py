import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import click
import yaml

from motor_driver import MotorDriver
from pca9685 import PCA9685

class motor_driver_cli(cmd.Cmd):
    def __init__(self, config):
        self.intro = 'Motor CLI'
        self.prompt = 'Motors > '
        self.doc_header='Motor Cli (type help):'

        self.motors = {}
        for m in config['subsystems']['motors']:
            motor = MotorDriver(PCA9685(), m['pwm_io'], m['dir_io'], m['dir_io_type'])
            self.motors[m['id']] = motor

        cmd.Cmd.__init__(self)
    def emptyline(self):
        pass
    def do_end(self, args):
        return True
    def help_end(self, args):
        print("End session")
    do_EOF = do_end
    help_EOF = help_end
    def do_quit(self, args):
        return True
    def help_quit(self, args):
        print("Quit session")
    def do_reverse(self, args):
        channel = 1 if len(args) == 0 else int(args.split()[0])
        self.motors[channel].reverse()
    def do_stop(self, args):
        channel = 1 if len(args) == 0 else int(args.split()[0])
        self.motors[channel].stop()
    def do_speed(self, args):
        channel = int(args.split()[0])
        speed = int(args.split()[1])
        print(channel, speed)
        print(self.motors)
        self.motors[channel].set_speed(speed)

if __name__ == '__main__':
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    cli = motor_driver_cli(config)
    cli.cmdloop()

