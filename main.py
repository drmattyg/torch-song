from limit_switch import LimitSwitchMCP
from MCP import MCPInput
import click
import time
import RPi.GPIO as GPIO
from motor_driver import MotorDriver
from relay import Relay

@click.group()
def cli():
    pass

@cli.command()
def monitor():
    print("Monitoring test")
    mcp = MCPInput(0x27, 10)
    ls_list = []
    for b in range(0, 10):
        ls_list.append(LimitSwitchMCP(mcp, b))
    current_state = []
    while current_state != mcp.update():
        time.sleep(10.0/1000) # wait for MCP to settle
        current_state = mcp.update()
    while(True):
        state = mcp.update()
        if state != current_state:    
            print(list(enumerate(state)))
            current_state = state
            time.sleep(0.1)

    # set_bits = (x[0] for x in enumerate(ls_list) if not x[1].get_state_raw())

    # print(list(set_bits))

IGN = 8 
VALVE = 7
V_OPEN = 0
V_CLOSE = 1
IG_ON = 0
IG_OFF = 1
PWM = 18
DIR = 23
shutdown_callback = None

def valve(state):
    GPIO.output(VALVE, state)

def ignitor(state):
    GPIO.output(IGN, state)

@cli.command()
@click.argument("speed", type=click.IntRange(0, 100))
def runtest(speed):
    # Initialize valve and ignition
    GPIO.setmode(GPIO.BCM)
    ign = Relay(IGN)
    valve = Relay(VALVE)
    # GPIO.setup(IGN, GPIO.OUT)
    # GPIO.output(IGN, 1)
    # GPIO.setup(VALVE, GPIO.OUT)
    # GPIO.output(VALVE, 1)

    # initialize motor driver
    md = MotorDriver(PWM, DIR)
    md.set_direction(MotorDriver.FORWARD)
    md.set_speed(speed)

    # initialize mcp
    mcp = MCPInput(0x27, 10)
    # initialize limit switches
    limit_switch_list = [LimitSwitchMCP(mcp, channel) for channel in [0, 1]]

    def limit_switch_callback(state, channel):
        if state == False:
            md.reverse()
            valve.invert()

    for ls in limit_switch_list:
        ls.set_change_callback(limit_switch_callback)

    md.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        md.stop()
                GPIO.cleanup()
        for ls in limit_switch_list:
            ls.kill()


@cli.command()
@click.argument("speed", type=click.IntRange(0, 100))
@click.argument("direction", type=click.IntRange(0, 1))

def drivetest(speed, direction):
    try:
        md = MotorDriver(PWM, DIR)
        md.set_direction(direction)
        md.set_speed(speed)
        md.start()
        while True:
            pass
    except KeyboardInterrupt:
        md.stop()
                GPIO.cleanup()



if __name__ == '__main__':
    cli()

