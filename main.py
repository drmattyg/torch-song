from limit_switch import LimitSwitchMCP
from MCP import MCPInput
import click
import time
import RPi.GPIO as GPIO
from motor_driver import MotorDriver


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

IGN = 14
VALVE = 15
V_OPEN = 0
V_CLOSE = 1
IG_ON = 0
IG_OFF = 1
PWM = 24
DIR = 23
def valve(state):
	GPIO.output(VALVE, state)

def ignitor(state):
	GPIO.output(IGN, state)

@cli.command()
@click.argument("speed", type=click.IntRange(0, 100))
def runtest(speed):
	IGN = 14
	VALVE = 15
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(IGN, GPIO.OUT)
	GPIO.setup(VALVE, GPIO.OUT)
	while True:
		GPIO.output(IGN, 0)
		GPIO.output(VALVE, 0)
		time.sleep(0.5)
		GPIO.output(IGN, 1)
		time.sleep(0.5)
		GPIO.output(VALVE, 1)
		time.sleep(0.5)

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



if __name__ == '__main__':
	cli()