# Create your views here.
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.models import User
import urllib2, urllib
from django.shortcuts import *
from django.http import HttpResponse
from collaborate.tasklist.serializers import *
from collaborate.tasklist.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions

@csrf_exempt
@login_required(login_url="/accounts/login/")
def index(request):
    account_id = request.user.account
    tasklists = TaskList.objects.filter(account=account_id)

    return render_to_response('tasks/index.html', {'tasklists': tasklists, 'user': request.user}, context_instance=RequestContext(request))
    

class AccountTaskListView(generics.ListCreateAPIView):
    """
    return a list of tasklists assigned to the account given.
    """
    model = TaskList
    serializer_class = TaskListSerializer

    def get(self, request, pk, format=None):
        tasklists = TaskList.objects.filter(account=pk)
        s = TaskListSerializer(tasklists)
        return Response(s.data, status=status.HTTP_200_OK)

class TaskListTasksView(generics.ListAPIView):
    """
    return a list of full task objects for the give tasklist id
    """
    model = Task
    serializer_class = TaskSerializer

    def get(self, request, pk, format=None):
        tasklist = TaskList.objects.get(pk=pk)
        tasks = tasklist.get_tasks()
        s = TaskSerializer(tasks)
        return Response(s.data, status=status.HTTP_200_OK)

class TaskListListView(generics.ListCreateAPIView):
    """
    List all tasklists or create a new task list.
    """
    model = TaskList
    serializer_class = TaskListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TaskListDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a TaskList Instance
    """
    model = TaskList
    serializer_class = TaskListSerializer

class TasksList(generics.ListCreateAPIView):
    model = Task
    serializer_class = TaskSerializer

class TasksListDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Task
    serializer_class = TaskSerializer

