from django.db import models
from collaborate.issue_tracker.fields import PickledObjectField
from collaborate.billing.models import *
from collaborate import settings
import django.utils.simplejson as json
from django.contrib.auth.models import User

# Create your models here.

class Issue(models.Model):
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    name = models.CharField(max_length=120) 
    problem = models.TextField()
    STATUS_CHOICES = (
        ('O', 'Open'),
        ('F', 'Fixed'),
        ('P', 'Pending'),
        ('N', 'New'),
        ('R', 'Rejected'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    ISSUE_TYPE_CHOICES = (
        ('NF', 'New Feature Request'),
        ('D', 'Defect or Bug'),
    ) 
    issue_type = models.CharField(max_length=2, choices=ISSUE_TYPE_CHOICES, default='D')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    tags = models.CharField(max_length=255)
    manager = models.ForeignKey('IssueManager') 
    comments = PickledObjectField()

    def __unicode__(self):
        return self.name

    

class IssueManager(models.Model):
    """
    IssueManger allows for manipulation of issues.  Similar to a queue
    used elsewhere in this code base.  Each issue manager is assigned an
    account_id which traces back to the proper account object that this 
    entity belongs to.
    """
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    account = models.ForeignKey(Account)
    
    def get_issues(self):
        return Issue.objects.filter(manager=self.id)



