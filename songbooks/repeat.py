import yaml
import sys
import copy
num_repeats = int(sys.argv[1])
sb_y = yaml.load(sys.stdin.read())
sb = sb_y['songbook']
print("version: 1.0")
print("songbook:")
max_time = sb[-1]['start_at'] + sb[-1]['time']
min_time = sb[0]['start_at']
measure_time = max_time - min_time
for i in range(num_repeats):
	for measure in sb:
		m = copy.deepcopy(measure)
		m['start_at'] += measure_time*i
		for line in yaml.dump([m], default_flow_style=False).split("\n"):
			print("   " + line)


