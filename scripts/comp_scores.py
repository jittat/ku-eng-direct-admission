import sys

if len(sys.argv) != 3:
    print """usage python comm_scores.py [score1] [score2]
- score1 should be exported from the web
- score2 should be the score from NIETS"""
    quit()

def read_score(filename):
    scores = {}
    for line in open(filename).readlines():
        items = line.strip().split(',')
        scores[items[0]] = float(items[1])

    return scores

def main():
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    scores1 = read_score(filename1)    
    scores2 = read_score(filename2)

    total = 0
    correct = 0
    up = 0
    down = 0

    for nat_id, score in scores2.iteritems():
        if nat_id not in scores1:
            continue
        total += 1
        score1 = scores1[nat_id] 
        if score1 != score:
            print nat_id, score, score1
            if score > score1:
                up += 1
            else:
                down += 1
        else:
            correct += 1

    print "Correct:", correct, "from", total
    print "Up:", up, "Down:", down

if __name__ == '__main__':
    main()
