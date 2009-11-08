# _*_ encoding: utf-8 _*_

from django.core import mail
from django.test import TestCase, TransactionTestCase

from django.conf import settings

from application.models import Applicant, SubmissionInfo

class SubmissionTestCase(TransactionTestCase):

    pass
