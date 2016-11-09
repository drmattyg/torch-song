import MCP.mcp as mcp
import limit_switch.limit_switch as lsw
import time
print("Monitoring test")
mcp = mcp.MCPInput(0x27, 10)
ls_list = []

def cb(state, channel):
	print("{}: {}".format(state, channel))

for b in range(0, 10):
	ls = lsw.LimitSwitchMCP(mcp, b)
	ls.set_change_callback(cb)
	ls_list.append(ls)
try:
	while(True):
		mcp.update()
		time.sleep(0.01)
		# set_bits = (x[0] for x in enumerate(ls_list) if x[1].get_state_raw())
		# print(set_bits)
except KeyboardInterrupt:
	for ls in ls_list:
		ls.kill()