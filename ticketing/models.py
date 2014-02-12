from django.db import models
from ticketing.fields import PickledObjectField
import settings
import django.utils.simplejson as json
from django.contrib.auth.models import User
from billing.models import Account
# Create your models here.

class Ticket(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    subject = models.CharField(max_length=140)
    body = models.TextField()
    SEVERITY_CHOICES = (
        ('0', 'Normal'),
        ('1', 'Urgent'),
        ('2', 'Emergency'),
    )
    severity = models.CharField(max_length=1, choices=SEVERITY_CHOICES, default='0')
    STATUS_CHOICES = ( 
        ('O', 'Open'),
        ('C', 'Closed'),
        ('P', 'Pending'),
        ('N', 'New'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='O')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    queue = models.ForeignKey('TicketQueue')
    tags = models.CharField(max_length=255)
    comments = PickledObjectField()

    def __unicode__(self):
        return self.subject

    def add_comment(self, comment):
        """
        add a comment dictionary to the comments. This dicts will be added by the timestamp
        of when the comment was made.
        """
        self.comments[comment['timestamp']] = comment
        self.save()

    def get_comments(self):
        comments = self.comments
        return json.dumps(comments)
        
    def add_tag(self, tag):
        self.tags += tag
        self.save()

    def set_status(self, status):
        self.status = status
        self.save()

    def set_severity(self, severity):
        self.severity = severity
        self.save()
    
    def set_agent(self, agent):
        self.agent = agent
        self.save()
    

class TicketQueue(models.Model):
    """
    Class used to organize tickets to different queues based on certain
    user given criteria
    """
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=255)
    account = models.ForeignKey(Account)

    def __unicode__(self):
        return self.name
    
    def add_members(self, members):
        for member in members:
            self.members.add(member)
        self.save()
    
    def add_tickets(self, tickets):
        for ticket in tickets:
            self.tickets.add(ticket)
        
    def get_tickets(self):
        return Ticket.objects.filter(queue=self.id)

    def get_members(self):
        return self.members

    
