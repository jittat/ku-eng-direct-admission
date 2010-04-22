import codecs

input_filename = '/home/jittat/mydoc/directadm53/final-assignment.csv'
quota_filename = '/home/jittat/mydoc/directadm53/quota_app_id.txt'
output_filename = '/home/jittat/mydoc/directadm53/final-assignment-filtered.csv'

def read_quota():
    q_data = {}
    for l in codecs.open(quota_filename, encoding='utf-8', mode='r').readlines():
        l = l.strip()
        items = l.split('\t')
        q_data[items[0]]=l
    return q_data

def main():
    q_data = read_quota()
    outfile = codecs.open(output_filename, encoding='utf-8', mode='w')
    lines = codecs.open(input_filename, encoding='utf-8', mode='r').readlines()
    print >> outfile, lines[0].strip()
    for l in lines[1:]:
        items = l.strip().split(',')
        if items[0] in q_data:
            print 'OUT:', l.strip()
            print q_data[items[0]]
            continue

        print >> outfile, l.strip()

if __name__=='__main__':
    main()

            
        


