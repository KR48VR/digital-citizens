"""Write ix.js for Film 2 from the casebook's record of King's messages (docs/playbook/records/interactions.json):
every message's number, kind and task (the dots), and the full text of the messages the film shows.
Usage: python make_ix.py path/to/interactions.json ix.js"""
import json
import sys

SHOWN = {4, 10, 14, 19, 53, 71, 72, 79, 101, 127, 128, 148, 151, 166, 168, 169}
rows = json.load(open(sys.argv[1]))['rows']
dots = [{'n': r['n'], 'type': r['type'], 'task': r['task'], 'time': r['time']} for r in rows]
shown = {r['n']: {'king': r['king'], 'claude': r['claude'], 'time': r['time'], 'type': r['type']} for r in rows if r['n'] in SHOWN}
assert len(shown) == len(SHOWN), SHOWN - set(shown)
open(sys.argv[2], 'w').write('const IX = ' + json.dumps(dots) + ';\nconst IXT = ' + json.dumps(shown, ensure_ascii=False) + ';\n')
print(len(dots), 'messages;', len(shown), 'shown in full')
