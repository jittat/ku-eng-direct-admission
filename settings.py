# Django settings for adm project.

import os.path
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('YOURNAME', 'YOUREMAIL'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'onlineadmission',             # Or path to database file if using sqlite3.
        'USER': 'onlineadmission',             # Not used with sqlite3.
        'PASSWORD': 'o-adm-for-dev',         # Not used with sqlite3.
        }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Bangkok'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'th-th'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4gu3*=+#v_psiakiq7zy0wle2grl%q5=3c4+cq+93!3@sr61b%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'adm.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR,'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django_extensions',
    'south',
    'mailer',
    'adm.application',
    'adm.upload',
    'adm.review',
    'adm.commons',
    'adm.manual',
    'adm.supplement',
    'adm.result',
    'adm.confirmation',
    'adm.feature_switch'
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

####################################
# ADM settings
####################################

# Absolute path to statis media, e.g., css files.  Used in development
# with django.views.static.serve
STATIC_DOC_ROOT = MEDIA_ROOT

# used in redirect_to_index
INDEX_PAGE = 'start-page'

MAX_PASSWORD_REQUST_PER_DAY = 10
MAX_DOC_UPLOAD_PER_DAY = 100

FAKE_SENDING_EMAIL = False

HTTP_BASE_PATH = ''

MAX_UPLOADED_DOC_FILE_SIZE = 2000000

EMAIL_BACKEND = 'adm.commons.backends.phpmailer'
SEND_MAILS_THROUGH_DJANGO_MAILER = True
PHPMAILER_KEY = ''

########################
# options for admission
########################
ADMISSION_YEAR = 53

# This is crucial for round 2 admission to ensure distinct application
# numbers from round 1.
SUBMISSION_METHOD_APPLICATION_ID_OFFSET = 2

# maximum number of choices
MAX_MAJOR_RANK = 1

from datetime import datetime, timedelta

LOGIN_ENABLED = True

SUBMISSION_CHANGE_GRACE_PERIOD = timedelta(3)
SUBMISSION_CHANGE_GRACE_PERIOD_END = datetime(2009,12,11)
SUBMISSION_DEADLINE = datetime(2010,5,10)
SUPPLEMENT_DEADLINE = datetime(2010,5,10)
ROUND2_CONFIRMATION_DEADLINE = datetime(2010,5,13,17,02)

ACCEPT_ONLY_GRADUATED = False
VERIFIY_MINIMUM_SCORE = False

# path for storing uploaded images (for documents)
FORCE_UPLOAD_DOC = False
UPLOADED_DOC_PATH = os.path.join(PROJECT_DIR,'uploaded_docs')

EMAIL_HOST = ''

EMAIL_SENDER = ''

TEST_DATABASE_COLLATION = 'utf8_general_ci'

MAX_SUPPLEMENTS = 10

CACHE_BACKEND = 'locmem:///'

RESULT_SETS = [
    (1,'eligible', True, 'result/eligible.html'),
    (2,'admitted', False, 'result/admitted.html'),
    (3,'waitlist', False, 'result/waitlist.html')
    ]

DEFAULT_RESULT_SET_NAME = 'eligible'
SHOW_ADMISSION_RESULTS = False
SHOW_FINAL_ADMISSION_RESULTS = False

CONFIRMATION_HASH_MAGIC = 'confr2'

try:
    from settings_local import *
except ImportError:
    pass 

# this is for checking if some crucial option has been left off

class IncompleteSettingsException(Exception):
    pass

if HTTP_BASE_PATH=='':
    raise IncompleteSettingsException("HTTP_BASE_PATH")
if PHPMAILER_KEY=='':
    raise IncompleteSettingsException("PHPMAILER_KEY")
if EMAIL_HOST=='':
    raise IncompleteSettingsException("EMAIL_HOST")
