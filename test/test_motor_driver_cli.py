import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import click
import yaml

from motor_driver import MotorDriver

stream = open("conf/default.yml", "r")
items = yaml.load(stream)
motors = {}
motors_config = items['io']['motors']
for r in motors_config:
    motors[motors_config[r]['id']] = MotorDriver(motors_config[r]['pwm_pin'], motors_config[r]['dir_pin'])

class motor_cli(cmd.Cmd):
    def __init__(self, intro='Motor CLI', prompt='> '):
        self.intro=intro
        self.prompt=prompt
        self.doc_header='Motor Cli (type help):'
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
    def do_start(self, args):
        which = 1 if len(args) == 0 else int(args.split()[0])
        motors[which].start()
    def do_stop(self, args):
        which = 1 if len(args) == 0 else int(args.split()[0])
        motors[which].stop()
    def do_speed(self, args):
        which = int(args.split()[0])
        speed = int(args.split()[1])
        motors[which].set_speed(speed)
    def do_freq(self, args):
        which = int(args.split()[0])
        freq = int(args.split()[1])
        motors[which].set_freq(freq)

if __name__ == '__main__':
    cli = motor_cli()
    cli.cmdloop()

