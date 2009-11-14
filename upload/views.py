# -*- coding: utf-8 -*-
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django import forms
from django.core.files.uploadhandler import FileUploadHandler, StopUpload
from django.conf import settings

from commons.decorators import applicant_required
from commons.email import send_submission_confirmation_by_email
from commons.utils import random_string

from application.views.status import submitted_applicant_required

from application.models import Applicant
from models import AppDocs
from models import get_field_thumbnail_filename, get_doc_fullpath


MAX_UPLOADED_DOC_FILE_SIZE = settings.MAX_UPLOADED_DOC_FILE_SIZE

def get_session_key(request):
    progress_id = None
    if 'X-Progress-ID' in request.GET :
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        return "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
    else:
        return None

class UploadProgressSessionHandler(FileUploadHandler):
    """
    Tracks progress for file uploads.  The http post request must
    contain a header or query parameter, 'X-Progress-ID' which should
    contain a unique string to identify the upload to be tracked.

    Taken from http://www.djangosnippets.org/snippets/678/
    """

    def __init__(self, request=None):
        super(UploadProgressSessionHandler, self).__init__(request)
        self.session_key = None

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.content_length = content_length
        self.session_key = get_session_key(self.request)
        if self.session_key:
            self.request.session[self.session_key] = {
                'finished': False,
                'length': self.content_length,
                'uploaded' : 0
                }

    def new_file(self, field_name, file_name, content_type, content_length, charset=None):
        pass

    def receive_data_chunk(self, raw_data, start):
        if self.session_key:
            data = self.request.session[self.session_key]
            data['uploaded'] += self.chunk_size
            self.request.session[self.session_key] = data
            self.request.session.save()
            #print data
        return raw_data
    
    def file_complete(self, file_size):
        #print 'done', file_size
        pass

    def upload_complete(self):
        if self.session_key:
            self.request.session[self.session_key]['finished'] = True
            self.request.session.save()

@applicant_required
def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    session_key = get_session_key(request)
    if session_key:
        from django.utils import simplejson
        #print 'session_key:', session_key
        try:
            data = request.session[session_key]
        except:
            data = {'length': 1, 'uploaded': 0, 'finished': False}
        #print data
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseServerError(
            'Server Error: You must provide X-Progress-ID header or query param.')


class FileUploadForm(forms.Form):
    uploaded_file = forms.FileField()

def populate_upload_field_forms(app_docs, fields, required_fields=None):
    field_forms = {}
    for f in fields:
        field = AppDocs._meta.get_field_by_name(f)[0]

        has_thumbnail = False
        if app_docs!=None:
            field_value = app_docs.__getattribute__(f)
            if (field_value!=None) and (field_value.name!=''):
                has_thumbnail = True

        if (required_fields == None) or (f in required_fields):
            required = True
        else:
            required = False

        field_forms[f] = { 'name': f,
                           'field': field,
                           'required' :required,
                           'has_thumbnail': has_thumbnail,
                           'random_string': random_string(5),
                           'form': FileUploadForm() }
    return field_forms
     
   
# this is for showing step bar
UPLOAD_FORM_STEPS = [
    ('อัพโหลดหลักฐาน','upload-index'),
    ('แก้ข้อมูลการสมัคร','apply-personal-info'),
    ]

@applicant_required
def index(request, missing_fields=None):

    docs = request.applicant.get_applicant_docs_or_none()
    if docs==None:
        docs = AppDocs(applicant=request.applicant)
        docs.save()
        request.applicant.add_related_model('appdocs', save=True)

    fields = docs.get_upload_fields()
    field_forms = populate_upload_field_forms(docs, 
                                              fields,
                                              docs.get_required_fields())

    if 'errors' in request.session:
        try:
            uploaded_field_error = request.session['errors']
            del request.session['errors']
        except KeyError:
            uploaded_field_error = None
    else:
        uploaded_field_error = None

    form_step_info = { 'steps': UPLOAD_FORM_STEPS,
                       'current_step': 0,
                       'max_linked_step': 1 }
    return render_to_response("upload/form.html",
                              { 'applicant': request.applicant,
                                'field_forms': field_forms,
                                'form_step_info': form_step_info,
                                'missing_fields': missing_fields,
                                'uploaded_field_error': uploaded_field_error })


def save_as_temp_file(f):
    """
    takes django memory uploaded file and saves to a temp file.
    """
    data = f.read()
    name = f.name
    from tempfile import mkstemp
    from django.core.files import File
    fid, temp_filename = mkstemp()
    #print fid, temp_filename
    new_f = os.fdopen(fid,'wb')
    new_f.write(data)
    new_f.close()
    f = File(open(temp_filename))
    f.name = name
    return (f, temp_filename)


def create_thumbnail(applicant, field_name, filename):
    thumb_filename = get_field_thumbnail_filename(field_name)
    full_thumb_filename = get_doc_fullpath(applicant, 
                                           thumb_filename)
    import Image
    size = 50,40
    im = Image.open(filename)
    im.thumbnail(size)

    dirname = os.path.dirname(full_thumb_filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    im.save(full_thumb_filename,'png')

def serve_file(filename):
    import mimetypes
    import stat
    from django.utils.http import http_date

    statobj = os.stat(filename)
    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    contents = open(filename, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    response["Content-Length"] = len(contents)
    return response


@applicant_required
def doc_thumbnail(request, field_name):
    if not AppDocs.valid_field_name(field_name):
        return HttpResponseServerError('Invalid field')

    docs = request.applicant.get_applicant_docs_or_none()
    if docs!=None:
        filename = docs.thumbnail_path(field_name)
        if os.path.exists(filename):
            return serve_file(filename)
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()


def upload_error(request, msg):
    request.session['errors'] = msg
    return HttpResponseRedirect(reverse('upload-index'))


@applicant_required
def upload(request, field_name):
    if request.method!="POST":
        return HttpResponseServerError('Bad request method')

    fields = AppDocs.FormMeta.upload_fields

    if not AppDocs.valid_field_name(field_name):
        return HttpResponseServerError('Invalid field')

    applicant = request.applicant

    docs = applicant.get_applicant_docs_or_none()
    request.upload_handlers.insert(0, UploadProgressSessionHandler(request))
    form = FileUploadForm(request.POST, request.FILES)
    uploaded_field_error = None
    if form.is_valid():
        f = request.FILES['uploaded_file']

        # check file size limit
        if f.size > MAX_UPLOADED_DOC_FILE_SIZE:
            uploaded_field_error = (
                "แฟ้มของ%s มีขนาดใหญ่เกินไป" % 
                (AppDocs.get_verbose_name_from_field_name(field_name),)
                )
            return upload_error(request, uploaded_field_error)

        # check upload quota
        if docs==None:
            docs = AppDocs()
            docs.applicant = applicant

        if not docs.can_upload_more_files():
            error = (
                ("คุณไม่สามารถอัพโหลดแฟ้มเพิ่มได้ "
                 "เนื่องจากในวันนี้คุณได้อัพโหลดแล้วทั้งสิ้นรวม %d ครั้ง "
                 "ให้รออัพโหลดใหม่ในวันพรุ่งนี้")
                % (settings.MAX_DOC_UPLOAD_PER_DAY,))
            return upload_error(request, error)
            
        # copy file
        used_temp_file = False

        # check if it's a file on disk
        try:
            temp_filename = f.temporary_file_path()
        except:
            # memory file... have to save it
            f, temp_filename = save_as_temp_file(f)
            used_temp_file = True

        # try to create a thumbnail
        try:
            create_thumbnail(applicant, field_name, temp_filename)
            if docs.__getattribute__(field_name):
                # clean old file
                docs.__getattribute__(field_name).delete(save=False)
            docs.__setattr__(field_name, f)

        except Exception:
            # bad uploaded file

            uploaded_field_error = (
                "แฟ้มรูปของ%s ที่อัพโหลดผิดรูปแบบ" %
                (AppDocs.get_verbose_name_from_field_name(field_name),)
                )
            if docs.__getattribute__(field_name):
                # clean the file
                docs.__getattribute__(field_name).delete(save=False)
            docs.__setattr__(field_name, None)

        docs.update_upload_counter()
        docs.save()
        applicant.add_related_model('appdocs', save=True)

        f.close()
        if used_temp_file:
            os.remove(temp_filename)

    if uploaded_field_error==None:
        return HttpResponseRedirect(reverse('upload-index'))
    else:
        return upload_error(request, uploaded_field_error)

@applicant_required
def submit(request):
    applicant = request.applicant
    if request.method!='POST':
        return HttpResponseRedirect(reverse('upload-index'))
        
    if applicant.appdocs.is_complete():
        try:
            applicant.submit(Applicant.SUBMITTED_ONLINE)
        except Applicant.DuplicateSubmissionError:
            return render_to_response(
                'commons/submission_already_submitted.html',
                { 'applicant': applicant })

        send_submission_confirmation_by_email(applicant)
        return render_to_response('upload/submission_success.html',
                                  { 'applicant': applicant })
    else:
        missing_fields = applicant.appdocs.get_missing_fields()
        missing_field_names = [
            AppDocs.get_verbose_name_from_field_name(f)
            for f in missing_fields
            ]
        return index(request, missing_field_names)


# this is for showing step bar
SHOW_UPLOAD_FORM_STEPS = [
    ('ดูข้อมูลที่ใช้สมัคร','status-show'),
    ('ดูหลักฐานที่อัพโหลดแล้ว','upload-show'),
    ]

@submitted_applicant_required
def show(request):
    docs = request.applicant.get_applicant_docs_or_none()
    fields = docs.get_upload_fields()
    field_forms = populate_upload_field_forms(docs, fields)

    form_step_info = { 'steps': SHOW_UPLOAD_FORM_STEPS,
                       'current_step': 1,
                       'max_linked_step': 1 }
    return render_to_response("upload/show.html",
                              { 'applicant': request.applicant,
                                'field_forms': field_forms,
                                'form_step_info': form_step_info })
