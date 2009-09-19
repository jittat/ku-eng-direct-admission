from django.http import HttpResponseRedirect
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

def index(request):
    return HttpResponseRedirect(reverse('upload-form'))

def upload(request):
    if request.method=="POST":
        request.upload_handlers.insert(0, TestUploadHandler())
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
