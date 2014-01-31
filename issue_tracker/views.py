# Create your views here.
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import *
from django.http import HttpResponse
from collaborate.issue_tracker.serializers import *
from collaborate.issue_tracker.models import *
from django.views.decorators.cache import cache_control, cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from django.core.cache import cache



def issues_client_index(request):
    account_id = request.user.get_profile().account
    issue_managers = IssueManager.objects.filter(account=account_id)
    
    return render_to_response('issues/index.html', {'managers': issue_managers})

class IssueManagerListView(generics.ListCreateAPIView):
    
    model = IssueManager
    serializer_class = IssueManagerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class IssueManagerDetailView(generics.RetrieveUpdateAPIView):
    
    model = IssueManager
    serializer_class = IssueManagerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    

class IssueListView(generics.RetrieveUpdateDestroyAPIView):
    model = Issue
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_obj(self, pk):
        try:
            return Issue.objects.get(pk=pk)
        except Issue.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_obj(pk)
        s = IssueSerializer(obj)
        if s.is_valid():
            return Response(s.data, status=status.HTTP_200_OK)
        else:
            raise Http502

        

class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Issue
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

