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
      'pat3': ScoreStat(103.19, 42.46, 276) },
    { 'gat': ScoreStat(128.43, 61.32, 300),
      'pat1': ScoreStat(56.26, 25.92, 300),
      'pat3': ScoreStat(83.54, 35.78, 300) },
    { 'gat': ScoreStat(139.38, 67.85, 300),
      'pat1': ScoreStat(48.34, 23.45, 300),
      'pat3': ScoreStat(121.25, 41.56, 300) }
    ]
EXAM_COUNT = len(SCORE_STATS)

class ApplicantScore:
    """Extract applicant's score from a string, and calculate
    normalized score.
    
    It is created from a line in score export, which can be a GAT/PAT line:

    >>> a = ApplicantScore("1350100262126,0,0,0,124.0,174.0,155.0,187.06,96.0,108.0,203.62,114.0,123.0,246.5,190.0,171.0,251.0,96.0,198.0")
    >>> a.nat_id
    '1350100262126'
    >>> a.scores
    {'pat1': [0.0, 174.0, 96.0, 114.0, 190.0, 96.0], 'pat3': [0.0, 155.0, 108.0, 123.0, 171.0, 198.0], 'gat': [0.0, 124.0, 187.06, 203.62, 246.5, 251.0]}

    Then, if you're using GAT/PAT, you can use it to calculate the
    normalized score.

    >>> c = ApplicantScore("1,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200")
    >>> print round(c.get_best_normalized_score('gat'),7)
    0.6719173
    >>> print round(c.get_best_normalized_score('pat1'),7)
    0.9042111
    >>> print round(c.get_best_normalized_score('pat3'),7)
    0.7873123
    >>> print round(c.get_score(),3)
    7876.882

    >>> d = ApplicantScore("1,250,250,250,250,250,250,250,250,250,250,250,250,250,250,250,250,250,250")
    >>> print round(d.get_score(),3)
    9020.444

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
