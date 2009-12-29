# -*- coding: utf-8 -*-
"""
This script converts score from GPS csv to the format suitable for
computing KU Eng normalized score.
"""
import codecs
import sys

file_name = sys.argv[1]
output_name = sys.argv[2]

HEAD_SKIP = 14

columns = [('nat_id', 2), 
           ('first_name', 5),
           ('last_name', 6),
           ('round', 11),
           ('gat',34), 
           ('pat1',12), 
           ('pat3', 15)]

pos = {'gat': 0, 'pat1': 1, 'pat3': 2}

def extract_columns(line):
    result = {}
    items = line.split(',')
    for c in columns:
        result[c[0]] = items[c[1]-1]
    return result

f = codecs.open(file_name, encoding='utf-8', mode='r')
fout = codecs.open(output_name, encoding='utf-8', mode='w')

lines = f.readlines()
lines = lines[14:]

scores = {}
full_name = {}

for l in lines:
    result = extract_columns(l)

    if result['nat_id'] == '':
        result['nat_id'] = old_result['nat_id']
        result['first_name'] = old_result['first_name']
        result['last_name'] = old_result['last_name']

    #print result['first_name'], result['last_name'], result['gat'], result['pat1'], result['pat3']

    nat_id = result['nat_id']
    if nat_id not in scores:
        scores[nat_id] = [0] * 9
        full_name[nat_id] = (result['first_name'], result['last_name'])

    r = int(result['round'][-1]) - 1
    for p,i in pos.iteritems():
        try:
            scores[nat_id][r * 3 + i] = float(result[p])
        except:
            pass

    old_result = result

for nat_id in scores.iterkeys():
    print >> fout, u'%s,%s,%s,%s' % (
        nat_id,
        full_name[nat_id][0],
        full_name[nat_id][1],
        ','.join([str(f) for f in scores[nat_id]]))

fout.close()
        
