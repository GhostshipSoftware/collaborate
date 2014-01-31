from django.forms import widgets
from rest_framework import serializers
from collaborate.tasklist.models import *

class TaskSerializer(serializers.ModelSerializer):

    body = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    due_date = serializers.DateTimeField(required=False)
    list = serializers.PrimaryKeyRelatedField(required=False)
    owner = serializers.PrimaryKeyRelatedField(required=False)


    class Meta:
        model = Task
    
    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.title = attrs.get('title', instance.title)
            instance.body = attrs.get('body', instance.body)
            instance.list = attrs.get('list', instance.list)
            instance.due_date = attrs.get('due_date', instance.due_date)
            instance.completed = attrs.get('completed', instance.completed)
            instance.owner = attrs.get('owner', instance.owner)
            instance.list = attrs.get('list', instance.list)
            return instance
        return Task(**attrs)

class TaskListSerializer(serializers.ModelSerializer):

    tasks = serializers.SerializerMethodField('get_tasks')
    
    class Meta:
        model = TaskList

    def get_tasks(self, obj):
        tasks = obj.get_tasks()
        return tasks

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.title = attrs.get('title', instance.title)
            return instance
        return TaskList(**attrs)


