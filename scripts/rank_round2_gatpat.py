import codecs
import sys

if len(sys.argv) != 5:
    print "usage python rank_round2_gatpat.py [app] [major] [cal-scores] [output]"
    quit()

def read_csv(f, key_index, index_names=None):
    data = {}
    for line in f.readlines():
        items = line.strip().split(',')
        if len(items)>key_index:
            if index_names==None:
                data[items[key_index]] = items
            else:
                d = {}
                for i in index_names.keys():
                    d[index_names[i]] = items[i]
                data[items[key_index]] = d
    return data

def read_scores(f):
    return read_csv(f,0, {0: 'nat_id', 1: 'score'})

def read_majors(f):
    return read_csv(f,1, {0: 'app_id', 1: 'nat_id', 3: 'major'})

def read_apps(f):
    return read_csv(f,0, 
                    { 0: 'app_id', 
                      1: 'nat_id', 
                      2: 'first_name', 
                      3: 'last_name' })
    

app_filename = sys.argv[1]
major_filename = sys.argv[2]
scores_filename = sys.argv[3]
output_filename = sys.argv[4]

f_app = codecs.open(app_filename, encoding='utf-8', mode='r')
f_maj = codecs.open(major_filename, encoding='utf-8', mode='r')
f_scores = codecs.open(scores_filename, encoding='utf-8', mode='r')
fout = codecs.open(output_filename, encoding='utf-8', mode='w')

apps = read_apps(f_app)
scores = read_scores(f_scores)
majors = read_majors(f_maj)

print scores.items()

nat_ids_by_scores = [t[1] for t in 
                     sorted([(-float(s[1]['score']),s[1]['nat_id']) 
                             for s in scores.items()])]

major_list = {}
for nat_id in nat_ids_by_scores:
    if not majors.has_key(nat_id):
        print "Error:", nat_id, "has not major pref"
        continue
    
    major = majors[nat_id]['major']

    if not major_list.has_key(major):
        major_list[major] = []

    major_list[major].append(majors[nat_id]['app_id'])

for m in major_list.keys():
    print "==============",m,"================"
    print >> fout, "==============",m,"================"
    for app_id in major_list[m]:
        if not apps.has_key(app_id):
            print "Error", app_id, "does not have app info"
            continue

        app = apps[app_id]
        score = scores[app['nat_id']]
        
        print >> fout, "%s,%s,%s,%s" % (app_id, app['first_name'], app['last_name'], score['score'])

fout.close()
