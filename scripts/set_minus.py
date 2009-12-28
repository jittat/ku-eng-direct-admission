# -*- coding: utf-8 -*-
import codecs
import sys

if len(sys.argv)!=5:
    print """Usage: python set_minus.py [set1.csv] [set2.csv] [out.csv] [field_number]

This script will output set1 - set2 (using field #field_number as key),
and save to [out.csv].  Note that field_number starts with 1."""
    quit()

set1_name = sys.argv[1]
set2_name = sys.argv[2]
out_name = sys.argv[3]
field_number = int(sys.argv[4]) - 1

def read_set(file_name):
    f = codecs.open(file_name, encoding="utf-8", mode="r")
    lines = f.readlines()
    return [line.strip().split(',') for line in lines]

def key_set(items, field_number):
    return set([i[field_number] for i in items])

def main():
    items1 = read_set(set1_name)
    items2 = read_set(set2_name)
    keys = key_set(items2, field_number)
    out_items = [i for i in items1 if i[field_number] not in keys]
    
    fout = codecs.open(out_name, encoding='utf-8', mode='w')
    for oi in out_items:
        print >> fout, ','.join(oi)
    fout.close()

if __name__ == '__main__':
    main()
