from limit_switch import LimitSwitch

i = 0

def cb(val):
	global i
	print("{}: {}".format(i, val))
	i = i + 1

ls = LimitSwitch(26)
ls.set_change_callback(cb)
try:
	while ls.thread_is_alive():
		pass
except KeyboardInterrupt:
	ls.kill()
	ls._thread.join()
	