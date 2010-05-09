# -*- coding: utf-8 -*-
"""
This script converts score from GPS csv to the format suitable for
computing KU Eng normalized score.
"""
import codecs
import sys

BASE_YEAR = 2552
EXAM_PER_YEAR = 3
EXAM_COUNT = 4

file_name = sys.argv[1]
output_name = sys.argv[2]

columns = [('nat_id', 2), 
           ('first_name', 3),
           ('last_name', 4),
           ('year',6),
           ('round', 7),
           ('subject',8), 
           ('score_type',9), 
           ('score', 10)]

def extract_columns(line):
    result = {}
    items = line.strip().split(',')
    if len(items)!=10:
        return None
    for c in columns:
        result[c[0]] = items[c[1]-1]
    return result

SCORE_POS = {'GAT ': 0, 'PAT 1 ': 1, 'PAT 3 ': 2}
SUBJECT_COUNT = len(SCORE_POS.keys())

def score_pos(year, r, subject):
    ri = int(r[-1])
    exam_num = (int(year) - BASE_YEAR) * EXAM_PER_YEAR + ri
    for s in SCORE_POS.keys():
        if subject.startswith(s):
            return (exam_num - 1) * SUBJECT_COUNT + SCORE_POS[s]
    return -1
    

f = codecs.open(file_name, encoding='utf-8', mode='r')
fout = codecs.open(output_name, encoding='utf-8', mode='w')

lines = f.readlines()
lines = lines[1:]

scores = {}
full_name = {}

for l in lines:
    result = extract_columns(l)

    if result==None:
        print 'BAD LINE:', l
        continue

    if result['score_type']!=u'คะแนนรวม':
        continue

    nat_id = result['nat_id']
    if nat_id not in scores:
        scores[nat_id] = [0] * EXAM_COUNT * SUBJECT_COUNT
        full_name[nat_id] = (result['first_name'], result['last_name'])

    p = score_pos(result['year'], result['round'], result['subject'])
    if (p!=-1) and (result['score']!='-'):
        scores[nat_id][p] = float(result['score'])

for nat_id in scores.iterkeys():
    print >> fout, u'%s,%s' % (
        nat_id,
        ','.join([str(f) for f in scores[nat_id]]))

fout.close()
        
