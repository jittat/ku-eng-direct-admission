import os

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django import forms
from django.core.files.uploadhandler import FileUploadHandler

from commons.decorators import applicant_required

from models import AppDocs

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


def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    session_key = get_session_key(request)
    if session_key:
        from django.utils import simplejson
        print 'session_key:', session_key
        try:
            data = request.session[session_key]
        except:
            data = {'length': 1, 'uploaded': 1, 'finished': True}
        #print data
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseServerError(
            'Server Error: You must provide X-Progress-ID header or query param.')


class FileUploadForm(forms.Form):
    uploaded_file = forms.FileField()

def populate_upload_field_forms(fields):
    field_forms = []
    for f in fields:
        field = AppDocs._meta.get_field_by_name(f)[0]
        field_forms.append({ 'name': f,
                             'field': field,
                             'form': FileUploadForm() })
    return field_forms
     
def get_applicant_docs_or_none(applicant):
    try:
        docs = applicant.appdocs
    except AppDocs.DoesNotExist:
        docs = None
    return docs
   
@applicant_required
def index(request):
    fields = AppDocs.FormMeta.upload_fields
    field_forms = populate_upload_field_forms(fields)

    docs = get_applicant_docs_or_none(request.applicant)

    return render_to_response("upload/form.html",
                              { 'field_forms': field_forms })


@applicant_required
def upload(request, field_name):
    if request.method!="POST":
        return HttpResponseServerError('Bad request method')

    fields = AppDocs.FormMeta.upload_fields

    if field_name not in fields:
        return HttpResponseServerError('Invalid field')

    docs = get_applicant_docs_or_none(request.applicant)
    request.upload_handlers.insert(0, UploadProgressSessionHandler(request))
    form = FileUploadForm(request.POST, request.FILES)
    if form.is_valid():
        f = request.FILES['uploaded_file']
        used_temp_file = False
        try:
            # check if it's a file on disk
            print "File is at:", f.temporary_file_path()
            pass
        except:
            # memory file... have to save it
            print "saving..."
            data = f.read()
            name = f.name
            print 'name:', f.name
            from tempfile import mkstemp
            from django.core.files import File
            fid, temp_filename = mkstemp()
            print fid, temp_filename
            new_f = os.fdopen(fid,'wb')
            new_f.write(data)
            new_f.close()
            f = File(open(temp_filename))
            f.name = name
            used_temp_file = True

        if docs==None:
            docs = AppDocs()
            docs.applicant = request.applicant

        docs.__setattr__(field_name, f)
        docs.save()

    if used_temp_file:
        f.close()
        os.remove(temp_filename)
    return HttpResponseRedirect(reverse('upload-index'))
