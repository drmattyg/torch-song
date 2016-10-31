from limit_switch import LimitSwitch

ls1 = LimitSwitch(26)
ls2 = LimitSwitch(19)
current_state1 = ls1.get_state_raw()
current_state2 = ls2.get_state_raw()
while True:
	state1 = ls1.get_state_raw()
	state2 = ls2.get_state_raw()
	if state1 != current_state1 :
		print(ls1.channel)
		print("\a")
		current_state1 = state1
	if state2 != current_state2:
		print(ls2.channel)
		print("\a")
		current_state2 = state2