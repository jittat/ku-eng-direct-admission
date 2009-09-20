from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django import forms
from django.core.files.uploadhandler import FileUploadHandler

class FileUploadForm(forms.Form):
    title = forms.CharField(max_length=100)
    uploaded_file = forms.FileField()

class TestUploadHandler(FileUploadHandler):
    def receive_data_chunk(self, raw_data, start):
        print "At:", start
        return raw_data
    
    def file_complete(self, file_size):
        print "Size:", file_size
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
        self.progress_id = None
        self.session_key = None

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.content_length = content_length
        if 'X-Progress-ID' in self.request.GET :
            self.progress_id = self.request.GET['X-Progress-ID']
        elif 'X-Progress-ID' in self.request.META:
            self.progress_id = self.request.META['X-Progress-ID']
        if self.progress_id:
            self.session_key = "%s_%s" % (self.request.META['REMOTE_ADDR'], self.progress_id )
            self.request.session[self.session_key] = {
                'length': self.content_length,
                'uploaded' : 0
                }
            print "added:", self.session_key

    def new_file(self, field_name, file_name, content_type, content_length, charset=None):
        pass

    def receive_data_chunk(self, raw_data, start):
        if self.session_key:
            data = self.request.session[self.session_key]
            data['uploaded'] += self.chunk_size
            self.request.session[self.session_key] = data
            print data
        return raw_data
    
    def file_complete(self, file_size):
        print 'done', file_size
        pass

    def upload_complete(self):
        if self.session_key:
            print self.session_key
            del self.request.session[self.session_key]




def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        from django.utils import simplejson
        session_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        try:
            data = request.session[session_key]
        except:
            data = {'length': 1, 'uploaded': 1}
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')



def index(request):
    return HttpResponseRedirect(reverse('upload-form'))

def upload(request):
    if request.method=="POST":
        request.upload_handlers.insert(0, UploadProgressSessionHandler(request))
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['uploaded_file']
            print f.content_type
            try:
                print f.temporary_file_path()
            except:
                print 'no path'
    else:
        form = FileUploadForm()
    return render_to_response("upload/form.html",
                              { 'form': form })
