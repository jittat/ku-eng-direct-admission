# -*- coding: utf-8 -*-
"""
This script converts score from GPS csv to the format suitable for
computing KU Eng normalized score.
"""
import codecs
import sys

BASE_YEAR = 2552
EXAM_PER_YEAR = 3
EXAM_COUNT = 6
NUM_SKIP = 14

file_name = sys.argv[1]
output_name = sys.argv[2]

columns = [('nat_id', 4), 
           ('first_name', 6),
           ('last_name', 9),
           ('year',12),
           ('round', 13),
           ('pat1',14),
           ('pat3',28),
           ('gat',48),
           ]

def extract_columns(line):
    result = {}
    items = line.strip().split(',')
    try:
        for c in columns:
            result[c[0]] = items[c[1]]
    except:
        print 'ERROR: ', line
        quit()
    return result

SCORE_POS = {'gat': 0, 'pat1': 1, 'pat3': 2}
SUBJECT_COUNT = len(SCORE_POS.keys())

def score_pos(year, r, subject):
    ri = int(r[-1])
    exam_num = (int(year) - BASE_YEAR) * EXAM_PER_YEAR + ri
    return (exam_num - 1) * SUBJECT_COUNT + SCORE_POS[subject]


f = codecs.open(file_name, encoding='utf-8', mode='r')
fout = codecs.open(output_name, encoding='utf-8', mode='w')

lines = f.readlines()
lines = lines[NUM_SKIP:]

scores = {}
full_name = {}

for l in lines:
    result = extract_columns(l)

    if result==None:
        print 'BAD LINE:', l
        continue

    nat_id = result['nat_id']
    if nat_id not in scores:
        scores[nat_id] = [0] * EXAM_COUNT * SUBJECT_COUNT
        full_name[nat_id] = (result['first_name'], result['last_name'])

    for n in SCORE_POS.keys():
        try:
            p = score_pos(result['year'], result['round'], n)
        except:
            print l
        if (p!=-1) and (result[n]!='-'):
            scores[nat_id][p] = float(result[n])

for nat_id in scores.iterkeys():
    print >> fout, u'%s,%s' % (
        nat_id,
        ','.join([str(f) for f in scores[nat_id]]))

fout.close()
        
