import yaml
import csv

def read_num_slots(file_name):
    f = open(file_name,'r')
    return yaml.load(f)

def read_applicant_scores(file_name):
    applicants = {}
    score_reader = csv.DictReader(open(file_name),['nat_id','score'])
    for app in score_reader:
        applicants[app['nat_id']] = float(app['score'])
    return applicants

def read_pref(file_name):
    prefs = {}
    pref_reader = csv.DictReader(open(file_name),
                                  ['id','nat_id','count'],
                                  'pref')
    for p in pref_reader:
        prefs[p['nat_id']] = p
    return prefs

def main():
    num_slots = read_num_slots('data/major_info.yaml')
    applicants = read_applicant_scores('data/score.csv')
    prefs = read_pref('data/pref.csv')

    majors = sorted(num_slots.keys())
    major_apps = {}
    full = {}
    upper_bound = {}
    lower_bound = {}
    missed = {}
    for m in majors:
        full[m] = False
        major_apps[m] = []
        upper_bound[m] = 0
        lower_bound[m] = 0
        missed[m] = 0
    nomajor = 0

    score_app = [(score,nat_id) for nat_id, score in applicants.iteritems()]
    # start processing, from higher scores
    for score, nat_id in sorted(score_app, reverse=True):
        pref = [int(pstr) for pstr in prefs[nat_id]['pref']]
        for p in pref:
            if not full[p]:
                major_apps[p].append(nat_id)
                lower_bound[p] = score
                if upper_bound[p] < score:
                    upper_bound[p] = score
                if len(major_apps[p]) == num_slots[p]:
                    full[p] = True
                break
            else:
                missed[p] += 1

    for m in majors:
        print "%3d %3d  %.2f  %.2f  %d" % (m, len(major_apps[m]), upper_bound[m], lower_bound[m], missed[m])

if __name__ == "__main__":
    main()


        
