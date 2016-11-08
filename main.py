from limit_switch import LimitSwitchMCP
from MCP import MCPInput

i = 0

print("Monitoring test")
mcp = MCPInput(0x27, 10)
ls_list = []
for b in range(0, 10):
	ls_list.append(LimitSwitchMCP(mcp, b))
mcp.update()
while(True):
	mcp.update()
	if mcp.all_true():
		continue
	set_bits = (x[0] for x in enumerate(ls_list) if x[1].get_state_raw())
	print(list(set_bits))
