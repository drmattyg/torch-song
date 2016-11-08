import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN)
GPIO.setup(26, GPIO.OUT)

print("0 -> 1")
GPIO.output(26, 0)
start = time.time()
GPIO.output(26, 1)
while(not GPIO.input(19)):
	pass
end = time.time()
print((end - start)*1000000)

print("1 -> 0")
start = time.time()
GPIO.output(26, 0)
while(GPIO.input(19)):
	pass
end = time.time()
print((end - start)*1000000)
