import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import cmd
import yaml

from torch_song.hardware import MotorDriver
from torch_song.hardware import PCA9685

class motor_driver_cli(cmd.Cmd):
    def __init__(self, config):
        self.last_motor = 1
        self.last_speed = 0
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
        channel = self.last_motor if len(args) == 0 else int(args.split()[0])
        self.motors[channel].reverse()
        print('Reversing Motor %d' % (channel))
    def do_stop(self, args):
        channel = self.last_motor if len(args) == 0 else int(args.split()[0])
        self.do_speed(str(channel) + " " + "0")
    def do_start(self, args):
        channel = self.last_motor if len(args) == 0 else int(args.split()[0])
        self.do_speed(str(channel) + " " + str(self.last_speed))
    def do_speed(self, args):
        print(args, self.last_speed)
        channel = self.last_motor if len(args.split()) == 1 else int(args.split()[0])
        speed = int(args.split()[0]) if len(args.split()) == 1 else int(args.split()[1])
        self.last_speed = speed
        print('Set Motor %d to speed %d' % (channel, speed))
        self.motors[channel].set_speed(speed)

if __name__ == '__main__':
    stream = open('conf/default.yml', 'r')
    config = yaml.load(stream)

    cli = motor_driver_cli(config)
    cli.cmdloop()

