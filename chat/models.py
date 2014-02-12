from django.db import models
from django.db import models
from ticketing.fields import PickledObjectField
from billing.models import *
from billing.serializers import *
import settings
import django.utils.simplejson as json
import jsonfield
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^collaborate\.ticketing\.fields\.PickledObjectField"])

class Message(models.Model):
    """
    Message object that defines each message sent to the server.
    """
    sent = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    msg = models.TextField()
    channel = models.ForeignKey('Channel')

    def get_username(self):
        return self.sender.username

class Channel(models.Model):
    """
    Object that holds all of the relevant information for each chat
    channel.
    """

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=255)
    members = jsonfield.JSONField(default={'users': []}, null=True, blank=True)
    account = models.ForeignKey(Account)
    motd = models.CharField(max_length=255)


    def __unicode__(self):
        return self.name

    def get_users(self):
        user_objs = []
        try:
            for m in self.members['users']:
                obj = BillingUser.objects.get(pk=m['id'])
                user_objs.append(obj)
        except TypeError:
            self.members = []
            self.save()
        return user_objs
       
    def add_user(self, user):
        if self.members is not None:
            if user in self.members['users']:
                return
            self.members['users'].append(user)
            self.save()

    def remove_user(self, user):
        for m in self.members['users']:
            if m['id'] == user['id']:
                self.members['users'].remove(user)
                break
        self.save()

    def get_messages(self, date_threshold=None):
        if date_threshold is None:
            msgs = Message.objects.filter(channel_id=self.id)
        else:
            msgs = Message.objects.filter(channel_id=self.id).filter(sent>=date_threshold)
        return msgs
