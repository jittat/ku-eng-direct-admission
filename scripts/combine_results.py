rounds = 3

base_filename = '../data/results_after_round%d.csv'

def read_results(filename):
    results = {}
    for l in open(filename).readlines():
        items = l.strip().split(',')
        results[items[0]] = (items[1],items[2])
    return results

def main():
    combined_results = {}
    for i in range(rounds):
        results = read_results(base_filename % (i+1))

        for n,res in results.items():
            combined_results[n] = res

    for n,res in combined_results.items():
        print "%s,%s,%s" % (n,res[0],res[1])


if __name__=='__main__':
    main()
