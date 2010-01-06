import sys

if len(sys.argv) != 3:
    print """usage python comm_raw_scores.py [score1] [score2]
- score1 should be exported from the web
- score2 should be the score from NIETS"""
    quit()

def read_score(filename):
    scores = {}
    for line in open(filename).readlines():
        items = line.strip().split(',')
        scores[items[0]] = [float(i) for i in items[3:]]

    return scores

def main():
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    scores1 = read_score(filename1)    
    scores2 = read_score(filename2)

    total = 0
    correct = 0
    down = 0
    
    for nat_id, score in scores2.iteritems():
        if nat_id not in scores1:
            continue
        total += 1
        score1 = scores1[nat_id] 

        is_correct = True
        is_down = False

        for s,s1 in zip(score,score1):
            if (s1!=0) and (s!=s1):
                is_correct = False
                if s1>s:
                    is_down = True


        if is_correct:
            correct += 1
        else:
            if is_down:
                down += 1
                print nat_id, score1, score

    print "Correct:", correct, "from", total, "| down:", down

if __name__ == '__main__':
    main()
