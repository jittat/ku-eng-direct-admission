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

def main():
    num_slots = read_num_slots('data/major_info.yaml')
    applicants = read_applicant_scores('data/score.csv')

if __name__ == "__main__":
    main()


        
