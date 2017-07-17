import random
from . import songbook_printer as sp
TIME_MIN = 5000
TIME_MAX = 12000
DUTY_CYCLE = 1/3
DIST_OPTS = [0.25, 0.33, 0.5, 0.66, 0.75, 1]
MEAN_DIST = sum(DIST_OPTS)/len(DIST_OPTS)
MEAN_TIME =int(MEAN_DIST*(TIME_MIN + TIME_MAX)/2)
NUM_EDGES = 9
NUM_CYCLES = 25

def sb_entry(edge, t, run_time, dist, direction=1):
    return [
        {
            'start_at': t,
            'time': run_time*dist,
            'edges': [{
                'edge': edge,
                'dir': direction,
                'distance': dist,
                'flame': 1
            }]
        },
        {
            'start_at': t + run_time*dist,
            'time': 100,
            'edges': [{
                'edge': edge,
                'dir': 0,
                'flame': 0
            }]
        }
    ]

t = 0
edges = {i: {'pos': 0, 'running': False, 'stop_at': -1} for i in range(NUM_EDGES)}
songbook = []
for i in range(NUM_CYCLES):
    for e in edges.values():
        if t > e['stop_at']:
            e['running'] = False
            e['stop_at'] = -1
    while True:
        edge = random.choice(range(NUM_EDGES))
        if not edges[edge]['running']:
            break
    dist = random.choice(DIST_OPTS)
    if e['pos'] == 1:
        direction = -1
    elif e['pos'] == 0:
        direction = 1
    else:
        direction = 1 - 2*random.choice([0, 1])
    end_pos = e['pos'] + direction*dist
    if end_pos < 0:
        end_pos = 0
        dist = e['pos']
    if end_pos > 1:
        end_pos = 1
        dist = 1 - e['pos']
    run_time = random.randint(TIME_MIN, TIME_MAX)
    songbook += sb_entry(edge, t, run_time, dist, direction=direction)
    edges[edge]['running'] = True
    edges[edge]['stop_at'] = t + run_time
    edges[edge]['pos'] = end_pos
    t += random.randint(int(TIME_MIN * DUTY_CYCLE), int(TIME_MIN * DUTY_CYCLE) + int(MEAN_TIME*DUTY_CYCLE))

songbook = {
    'author': 'Matt Gordon',
    'version': 1.0,
    'songbook': songbook
}
sp.songbook_printer(songbook)