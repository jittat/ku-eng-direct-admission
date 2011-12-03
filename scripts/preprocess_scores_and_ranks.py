import sys

score_filename = sys.argv[1]
pref_filename = sys.argv[2]

def read_csv(filename, min_items, process_items):
    results = {}
    lines = open(filename).readlines()
    for l in lines:
        items = l.strip().split(',')
        if len(items) < min_items:
            continue
        
        k,v = process_items(items)
        #print k

        results[k] = v

    return results


def read_pref(filename):

    def process_pref(items):
        r = items[3:]
        return items[1],r

    return read_csv(filename,3,process_pref)

def read_scores(filename):

    def process_score(items):
        return items[0], items[1]

    return read_csv(filename,2,process_score)


def main():
    prefs = read_pref(pref_filename)
    scores = read_scores(score_filename)

    slist = [(scores[nid], prefs[nid]) for nid in scores.keys()]

    final_list = sorted(slist,
                        lambda x,y: cmp(-float(x[0]),-float(y[0])))

    for s,r in final_list:
        mylist = r + ['0'] * (6 - len(r))

        print s + ' ' + ' '.join(mylist)


if __name__=='__main__':
    main()
        
