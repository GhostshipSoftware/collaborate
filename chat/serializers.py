from django.forms import widgets
from rest_framework import serializers
from chat.models import *



class ChannelSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField('get_users')
    class Meta:
        model = Channel
   
    def get_users(self, obj):
        users = obj.get_users()
        return users

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.name = attrs.get('name', instance.name)
            instance.description = attrs.get('description', instance.description)
            return instance
        return Channel(**attrs)

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username') 
    class Meta:
        model = Message
 
    def get_username(self, obj):
        username = obj.get_username()
        return username
        
    def restore_object(self, attrs, instance=None):
        if instance is not None:    
            instance.sent = attrs.get('sent', instance.sent)
            instance.msg = attrs.get('msg', instance.msg)
            instance.sender = attrs.get('sender', instance.sender)
            instance.channel = attrs.get('channel', instance.channel)
            return instance
        return Message(**attrs)
