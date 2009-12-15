from django.shortcuts import render_to_response

def deadline_passed_error(request):
    return render_to_response("commons/closed.html")

