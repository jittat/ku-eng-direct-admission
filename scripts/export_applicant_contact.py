from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from application.models import Applicant, PersonalInfo

ids = """1859900134827
1100800737277
1103701031581
1839900286864
1103700968954
1130300087028
1209700144999
1100500615281
2309800019000
1103700920391
1170600106907
1679900230097
1102001836381
1840100351914
1329900237264
1140800064078
1620400173703
1679900217651
1100200749967
1102400062665
1101800600108"""

def main():
    for i in ids.split("\n"):
        nat_id = i.strip()
        applicant = Applicant.objects.get(national_id=nat_id)
        personal_info = applicant.personal_info
        print (u'"%s","%s","%s","%s"' % 
               (nat_id, applicant,
                applicant.email,
                personal_info.phone_number))

if __name__ == '__main__':
    main()

