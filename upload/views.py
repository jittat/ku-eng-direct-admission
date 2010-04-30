# -*- coding: utf-8 -*-
import os

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django import forms
from django.core.files.uploadhandler import FileUploadHandler, StopUpload
from django.conf import settings

from commons.decorators import applicant_required, active_applicant_required
from commons.decorators import within_submission_deadline
from commons.utils import supplement_submission_deadline_passed

from commons.email import send_submission_confirmation_by_email, send_resubmission_confirmation_by_email
from commons.utils import random_string, serve_file, extract_variable_from_session_or_none

from application.views.status import submitted_applicant_required
from application.views.form_views import redirect_to_applicant_first_page

from application.models import Applicant

from review.models import ReviewField, ReviewFieldResult, CompletedReviewField

from models import AppDocs
from models import get_field_thumbnail_filename, get_field_preview_filename
from models import get_doc_fullpath


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
        return HttpResponseNotFound(
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

@within_submission_deadline
@active_applicant_required
def index(request, missing_fields=None):
    if not request.applicant.has_major_preference():
        return redirect_to_applicant_first_page(request.applicant)

    notice = extract_variable_from_session_or_none(request.session, 'notice')
    uploaded_field_error = extract_variable_from_session_or_none(
        request.session, 'error')

    docs = request.applicant.get_applicant_docs_or_none()
    if docs==None:
        docs = AppDocs(applicant=request.applicant)
        docs.save()
        request.applicant.add_related_model('appdocs', 
                                            save=True)

    completed_review_fields = CompletedReviewField.get_for_applicant(request.applicant)
    completed_review_field_names = [rf.short_name 
                                    for rf 
                                    in completed_review_fields]

    fields = docs.get_upload_fields()
    required_fields = docs.get_required_fields(
        excluded=completed_review_fields)

    if len(required_fields) == 0:
        return HttpResponseRedirect(reverse('upload-confirm'))

    field_forms = populate_upload_field_forms(docs, 
                                              fields,
                                              required_fields)

    form_step_info = { 'steps': UPLOAD_FORM_STEPS,
                       'current_step': 0,
                       'max_linked_step': 1 }
    return render_to_response("upload/form.html",
                              { 'applicant': request.applicant,
                                'field_forms': field_forms,
                                'form_step_info': form_step_info,
                                'notice': notice,
                                'missing_fields': missing_fields,
                                'completed_review_field_names':
                                    completed_review_field_names,
                                'uploaded_field_error':
                                    uploaded_field_error })


UPDATE_FORM_STEPS = [
    ('อัพโหลดหลักฐาน','upload-index'),
    ]

@submitted_applicant_required
def update(request, missing_fields=None):
    if not request.applicant.can_resubmit_online_doc():
        return HttpResponseForbidden()

    if supplement_submission_deadline_passed():
        return HttpResponseRedirect(reverse('commons-deadline-error'))

    notice = extract_variable_from_session_or_none(request.session, 'notice')
    uploaded_field_error = extract_variable_from_session_or_none(
        request.session, 'error')

    applicant = request.applicant

    if request.method=='POST':
        applicant.resubmit()
        send_resubmission_confirmation_by_email(applicant)
        return HttpResponseRedirect(reverse('status-index'))

    docs = applicant.get_applicant_docs_or_none()
    review_results = ReviewFieldResult.get_applicant_review_results(applicant)

    error_fields, error_results, passed_fields = [], [], []
    for result in review_results:
        if result.is_passed:
            passed_fields.append(result.review_field.name)
        else:
            error_fields.append(result.review_field.short_name)
            error_results.append(result)

    field_forms = populate_upload_field_forms(docs, 
                                              error_fields)

    # add reviewer comments
    for field, result in zip(error_fields, error_results):
        field_forms[field]['comment'] = result.applicant_note

    form_step_info = { 'steps': UPDATE_FORM_STEPS,
                       'current_step': 0,
                       'max_linked_step': 0 }
    return render_to_response("upload/update.html",
                              { 'applicant': request.applicant,
                                'field_forms': field_forms,
                                'passed_fields': passed_fields,
                                'form_step_info': form_step_info,
                                'notice': notice,
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
    # create thumbnail
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

    # create preview
    preview_filename = get_field_preview_filename(field_name)
    full_preview_filename = get_doc_fullpath(applicant, 
                                             preview_filename)

    im = Image.open(filename)
    if im.size[0] > im.size[1]:
        size = 400,300
    else:
        size = 300,400
    im.thumbnail(size)

    im.save(full_preview_filename,'png')


@applicant_required
def doc_get_img(request, field_name, thumbnail=True):
    if not AppDocs.valid_field_name(field_name):
        return HttpResponseNotFound('Invalid field')

    docs = request.applicant.get_applicant_docs_or_none()
    if docs!=None:
        if thumbnail:
            filename = docs.thumbnail_path(field_name)
        else:
            filename = docs.preview_path(field_name)
        if os.path.exists(filename):
            return serve_file(filename)
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()


def upload_error(request, msg, update=False):
    request.session['errors'] = msg
    if not update:
        return HttpResponseRedirect(reverse('upload-index'))
    else:
        return HttpResponseRedirect(reverse('upload-update'))


@applicant_required
def upload(request, field_name):
    if request.method!="POST":
        return HttpResponseForbidden('Bad request method')

    applicant = request.applicant
    if applicant.is_submitted:
        if not applicant.can_resubmit_online_doc():
            return HttpResponseForbidden('You have already submitted')
        if not ReviewFieldResult.is_field_with_error_result(applicant, field_name):
            return HttpResponseForbidden('You resubmitted on the wrong field')            

    fields = AppDocs.FormMeta.upload_fields

    if not AppDocs.valid_field_name(field_name):
        return HttpResponseNotFound('Invalid field')

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
        applicant.add_related_model('appdocs', 
                                    save=True,
                                    smart=True)

        f.close()
        if used_temp_file:
            os.remove(temp_filename)

    if uploaded_field_error==None:
        if not applicant.is_submitted:
            return HttpResponseRedirect(reverse('upload-index'))
        else:
            return HttpResponseRedirect(reverse('upload-update'))
    else:
        return upload_error(request, 
                            uploaded_field_error,
                            applicant.is_submitted)

@within_submission_deadline
@active_applicant_required
def submit(request):
    applicant = request.applicant
    if request.method!='POST':
        return HttpResponseRedirect(reverse('upload-index'))
        
    if applicant.appdocs.is_complete():
        return HttpResponseRedirect(reverse('upload-confirm'))
    else:
        missing_fields = applicant.appdocs.get_missing_fields()
        missing_field_names = [
            AppDocs.get_verbose_name_from_field_name(f)
            for f in missing_fields
            ]
        return index(request, missing_field_names)


@within_submission_deadline
@active_applicant_required
def confirm(request):
    applicant = request.applicant
    if ((not applicant.has_online_docs()) or
        (not applicant.appdocs.is_complete())):
        return HttpResponseRedirect(reverse('upload-index'))

    if request.method!='POST':
        docs = request.applicant.get_applicant_docs_or_none()
        fields = docs.get_upload_fields()
        completed_review_fields = CompletedReviewField.get_for_applicant(request.applicant)
        completed_review_field_names = [rf.short_name 
                                        for rf 
                                        in completed_review_fields]

        field_forms = populate_upload_field_forms(docs, fields)

        return render_to_response("upload/confirm.html",
                                  { 'applicant': request.applicant,
                                    'field_forms': field_forms,
                                    'completed_review_field_names':
                                        completed_review_field_names })

    else:
        if not 'submit' in request.POST:
            return render_to_response(
                'application/submission/not_submitted.html')

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
