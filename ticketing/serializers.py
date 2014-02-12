from django.forms import widgets
from rest_framework import serializers
from ticketing.models import *

class TicketSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField('get_comments')
    class Meta:
        model = Ticket
   
    def get_comments(self, obj):
        comments = obj.get_comments()
        return comments

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.subject = attrs.get('subject', instance.subject)
            instance.body = attrs.get('body', instance.body)
            instance.severity = attrs.get('severity', instance.severity)
            instance.status = attrs.get('status', instance.status)
            instance.agent = attrs.get('agent', instance.agent)
            instance.queue = attrs.get('queue', instance.queue)
            instance.tags = attrs.get('tags', instance.tags)
            return instance
        attrs['comments'] = {}
        return Ticket(**attrs)

class TicketCommentSerializer(serializers.ModelSerializer):
    body = serializers.CharField(required=False)
    tags = serializers.CharField(max_length=255, required=False)
    agent = serializers.RelatedField(required=False)
    subject = serializers.CharField(max_length=255, required=False)
    queue = serializers.RelatedField(required=False)

    class Meta:
        model = Ticket

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.subject = attrs.get('subject', instance.subject)
            instance.body = attrs.get('body', instance.body)
            instance.severity = attrs.get('severity', instance.severity)
            instance.status = attrs.get('status', instance.status)
            instance.agent = attrs.get('agent', instance.agent)
            instance.queue = attrs.get('queue', instance.queue)
            instance.tags = attrs.get('tags', instance.tags)
            instance.comments = attrs.get('comments', instance.comments)
            return instance
        return None

class TicketQueueSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField('get_tickets')

    def get_tickets(self, obj):
        tickets = obj.get_tickets()
        serialized_tickets = []
        for ticket in tickets:
            s = TicketSerializer(ticket)
            serialized_tickets.append(s.data)
        return serialized_tickets

    class Meta:
        model = TicketQueue

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.name = attrs.get('name', instance.name)
            instance.members = attrs.get('members', instance.members)
            instance.tickets = attrs.get('tickets', instance.tickets)
            instance.description = attrs.get('description', instance.description)
            instance.account = attrs.get('account_id', instance.account)
            return instance
        return TicketQueue(**attrs)

