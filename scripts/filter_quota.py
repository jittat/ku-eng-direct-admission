import codecs

input_filename = '/home/jittat/mydoc/directadm53/payment/assignment.csv'
quota_filename = '/home/jittat/mydoc/directadm53/payment/quota.txt'
output_filename = '/home/jittat/mydoc/directadm53/payment/assignment-added.csv'

def read_quota():
    q_data = {
        'nat_id': {},
        'firstname': {},
        'lastname': {}
        }
    for l in codecs.open(quota_filename, encoding='utf-8', mode='r').readlines():
        items = l.strip().split('\t')
        l = l.strip()
        if len(items)!=4:
            continue
        q_data['nat_id'][items[0]] = l
        if items[2] in q_data['firstname']:
            q_data['firstname'][items[2]].append(l)
        else:
            q_data['firstname'][items[2]] = [l]
            
        if items[3] in q_data['lastname']:
            q_data['lastname'][items[3]].append(l)
        else:
            q_data['lastname'][items[3]] = [l]
    return q_data

def main():
    q_data = read_quota()
    lines = codecs.open(input_filename, encoding='utf-8', mode='r').readlines()
    outfile = codecs.open(output_filename, encoding='utf-8', mode='w')
    for l in lines[1:]:
        items = l.strip().split(',')
        if items[1] in q_data['nat_id']:
            print 'OUT:', l.strip()
            print >> outfile, l.strip() + ',1,16000'
            continue

        print >> outfile, l.strip() + ',0,0'


        if items[3] in q_data['firstname']:
            print 'CHECK-LAST:', l.strip()
            for k in q_data['firstname'][items[3]]:
                print k
            print '------------------'
            continue

        if items[4] in q_data['lastname']:
            print 'CHECK-FIRST:', l.strip()
            for k in q_data['lastname'][items[4]]:
                print k
            print '------------------'
            continue

if __name__=='__main__':
    main()

            
        


