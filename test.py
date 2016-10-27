from limit_switch import LimitSwitch

ls = LimitSwitch(26)
ls.kill()
current_state = ls.get_state_raw()
while True:
	state = ls.get_state_raw()
	if state != current_state:
		print(state)
		current_state = state
	