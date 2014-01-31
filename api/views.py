# Our apps
from collaborate.tasklist.models import *
#

from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils import simplejson
from django.http import HttpResponse
import urllib2, urllib
from django.shortcuts import *

@csrf_exempt
def authenticate(request):
    user = request.user
    if request.method == "POST":
        #jobj = simplejson.loads()
        jobj = simplejson.loads(str(request.raw_post_data))
        username = jobj['credentials']['username']
        password = jobj['credentials']['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth.login(request, user)
                response = {"response": "login successful", "user": {"token": request.session.session_key}}
                return HttpResponse(simplejson.dumps(response), content_type="application/json")
            else:
                response = {"response": "Account has been deactivated."}
                return HttpResponse(simplejson.dumps(response), content_type="application/json", status='401')
        else:
            response = {"response": "No account found."}
            return HttpResponse(simplejson.dumps(response), content_type="application/json", status='401')
    else:
        response = {"response": "Incorrect Request Method"}
        return HttpResponse(simplejson.dumps(response), content_type="application/json", status='401')

def get_task_lists(request):
    user = request.user
    if request.method == "GET":
        
