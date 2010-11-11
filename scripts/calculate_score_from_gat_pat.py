# This script calculates scores for Round 2 of admission

import sys

class ScoreStat:

    SUPER_ZMAX = 8

    def __init__(self, mean, sd, max_score):
        self.mean = mean
        self.sd = sd
        self.max_score = max_score

    def cal_score(self, x):
        z = (x - self.mean) / self.sd
        return 0.5 + 0.5 * z / ScoreStat.SUPER_ZMAX

SCORE_STATS = [
    { 'gat': ScoreStat(78.09, 44.32, 290),
      'pat1': ScoreStat(88.33, 30.63, 300),
      'pat3': ScoreStat(108.66, 26.17, 240) },
    { 'gat': ScoreStat(93.10, 51.13, 287.5),
      'pat1': ScoreStat(87.11, 31.14, 300),
      'pat3': ScoreStat(97.86, 28.56, 260) },
    { 'gat': ScoreStat(106.78, 55.59, 292.5),
      'pat1': ScoreStat(63.56, 25.90, 270),
      'pat3': ScoreStat(86.73, 24.64, 237) },
    { 'gat': ScoreStat(130.82, 58.27, 295),
      'pat1': ScoreStat(63.97, 30.86, 294),
      'pat3': ScoreStat(103.19, 42.46, 276) }
    ]
EXAM_COUNT = len(SCORE_STATS)

class ApplicantScore:
    """Extract applicant's score from a string, and calculate
    normalized score.
    
    It is created from a line in score export, which can be a GAT/PAT line:

    >>> a = ApplicantScore("1949900170113,132.0,138.0,150.0,138.25,156.0,90.0,228.0,66.0,99.0,223.46,96.0,132.0")
    >>> a.nat_id
    '1949900170113'
    >>> a.scores
    {'pat1': [138.0, 156.0, 66.0, 96.0], 'pat3': [150.0, 90.0, 99.0, 132.0], 'gat': [132.0, 138.25, 228.0, 223.46000000000001]}

    >>> c = ApplicantScore("1,200,200,200,200,200,200,200,200,200,200,250,200")
    >>> print round(c.get_best_normalized_score('gat'),7)
    0.6719173
    >>> print round(c.get_best_normalized_score('pat1'),7)
    0.876762
    >>> print round(c.get_best_normalized_score('pat3'),7)
    0.7873123
    >>> print round(c.get_score(),3)
    7808.26

    """
    def __init__(self, st):
        items = st.split(',')
        self.nat_id = items[0]
        self.scores = ApplicantScore.extract_gatpat_scores(
            [float(s) for s in items[1:]])
        
    @staticmethod
    def extract_gatpat_scores(score_list):
        scores = {'gat': [0] * EXAM_COUNT,
                  'pat1': [0] * EXAM_COUNT,
                  'pat3': [0] * EXAM_COUNT}

        i = 0
        for e in range(EXAM_COUNT):
            for exam in ['gat','pat1','pat3']:
                scores[exam][e] = score_list[i]
                i += 1

        return scores

    def get_best_normalized_score(self, test_name):
        best_score = 0
        for i in range(EXAM_COUNT):
            x = self.scores[test_name][i]
            if x>300:
                print >> sys.stderr, "ERROR:", self.nat_id, test_name, x
            score = SCORE_STATS[i][test_name].cal_score(x)
            if score > best_score:
                best_score = score
        return best_score

    def get_score(self):
        gat = self.get_best_normalized_score('gat')
        pat1 = self.get_best_normalized_score('pat1')
        pat3 = self.get_best_normalized_score('pat3')
        score = (gat * 0.25 +
                 pat1 * 0.25 + 
                 pat3 * 0.5)
        return 10000.0 * score

def main():
    applicant_scores = []
    while True:
        try:
            line = raw_input()
            app = ApplicantScore(line)
            applicant_scores.append(app)
        except:
            break
    for app in applicant_scores:
        print "%s,%f" % (app.nat_id, app.get_score())

if __name__ == "__main__":
    main()
