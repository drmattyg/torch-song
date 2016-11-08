import MCP.mcp as mcp
import limit_switch.limit_switch as lsw
print("Monitoring test")
mcp = mcp.MCPInput(0x27, 10)
ls_list = []
for b in range(0, 10):
	ls[b] = lsw.LimitSwitchMCP(mcp, b)
mcp.update()
while(True):
	mcp.update()
	if mcp.all_true():
		continue
	set_bits = (x[0] for x in enumerate(ls_list) if x[1].get_state_raw())
	print(set_bits)
