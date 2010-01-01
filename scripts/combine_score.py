import sys
import csv

score_filename = sys.argv[1]
niets_filename = sys.argv[2]

gpaxs = {}

def main():
    # read gpax from score from export_score
    sreader = csv.reader(open(score_filename))
    for row in sreader:
        is_gatpat = row[2] == 'gatpat'
        if is_gatpat:
            nat_id, gpax = row[0], row[1]
            gpaxs[nat_id] = gpax

    for row in csv.reader(open(niets_filename)):
        nat_id = row[0]

        if nat_id in gpaxs:
            new_rows = [nat_id, gpaxs[nat_id], 'gatpat'] + row[3:]
            print ','.join([str(f) for f in new_rows])


if __name__ == '__main__':
    main()


