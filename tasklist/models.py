from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager,AbstractUser
from collaborate.billing.models import *
from collaborate import settings

    
# Create your models here.

class Task(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    list = models.ForeignKey('TaskList')
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    due_date = models.DateTimeField()
    

    def __unicode__(self):
        return self.title


    def complete(self):
        self.completed = True
        self.save()


    
class TaskList(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.CharField(max_length=200)
    account = models.ForeignKey(Account)
    

    def __unicode__(self):
        return self.title


    def get_tasks(self):
        tasks = Task.objects.filter(list=self.id)
        return tasks



