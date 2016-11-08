import Adafruit_GPIO.MCP230xx as MCP
import Adafruit_GPIO as GPIO
import time
import click
import RPi.GPIO as RGPIO

mcp = MCP.MCP23017(busnum = 1, address = 0x27)

@click.group()
def cli():
	pass

@cli.command()
@click.argument('bit_num', type=int)
def blink(bit_num):
	mcp.setup(bit_num, GPIO.OUT)
	while True:
		mcp.output(bit_num, 1)
		time.sleep(0.5)
		mcp.output(bit_num, 0)
		time.sleep(0.5)

@cli.command()
@click.argument('b', type=int)
def bit_read(b):
	mcp.setup(b, GPIO.IN)
	while True:
		print(mcp.input(b))
		time.sleep(0.5)

@cli.command()
def monitor():
	bits = range(0, 16)
	bit_vals = range(0, 16)
	for b in bits:
		mcp.setup(b, GPIO.IN)
                mcp.pullup(b, True)
		bit_vals[b] = mcp.input(b) # clear the first read
		bit_vals[b] = mcp.input(b)  
	while True:
		for b in bits:
			v = mcp.input(b)
			if v != bit_vals[b]:
				print("{}: {}".format(b, v))
				bit_vals[b] = v
			time.sleep(1/10000)

@cli.command()
def timing():
	RGPIO.setmode(RGPIO.BCM)
	RGPIO.setup(26, RGPIO.OUT)
	RGPIO.output(26, 0)
	mcp.setup(0, GPIO.OUT)
	while mcp.input(0):
		pass
	print("0 -> 1")
	start = time.time()
	RGPIO.output(26, 1)
	while not mcp.input(0):
		pass
	end = time.time()
	print((end - start)*1000000)

	print("1 -> 0")
	start = time.time()
	RGPIO.output(26, 0)
	while mcp.input(0):
		pass
	end = time.time()
	print((end - start)*1000000)



if __name__ == '__main__':
	cli()

