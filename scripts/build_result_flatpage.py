# -*- coding: utf-8 -*-
import codecs
import sys

is_forced = False
if '--force' in sys.argv:
    is_forced = True
    i = sys.argv.index('--force')
    del sys.argv[i]

if len(sys.argv)!=3:
    print "Usage: python build_result_flatpage.py [url] [results.csv] [--force]"
    quit()
url = sys.argv[1]
file_name = sys.argv[2]

from django.conf import settings
from django_bootstrap import bootstrap
bootstrap(__file__)

from django.template.loader import get_template
from django.template import Context
from django.contrib.flatpages.models import  FlatPage

def read_results():
    f = codecs.open(file_name, encoding="utf-8", mode="r")
    lines = f.readlines()
    order = 1
    applicants = []
    for l in lines:
        items = l.split(',')
        app = {'order': order,
               'ticket_number': items[0],
               'first_name': items[1],
               'last_name': items[2] }
        applicants.append(app)
        order += 1
    return applicants

def main():
    applicants = read_results()
    flatpages = FlatPage.objects.filter(url=url)
    if len(flatpages)==0:
        flatpage = FlatPage(url=url)
    elif is_forced:
        flatpage = flatpages[0]
    else:
        print "\nError: old flatpage exists.  Use --force to force overwrite."
        quit()

    template = get_template('result/include/applicant_list.html')
    context = Context({'applicants': applicants})
    flatpage.title = u'ประกาศ'
    flatpage.content = template.render(context)
    flatpage.template_name = 'flatpages/result.html'
    flatpage.save()

    print """.....
Done.
The script only created a flatpage at %s for you.  
You'll have to set the title, its sites, 
and edit other part of the page yourself.""" % (url,)

if __name__ == '__main__':
    main()
