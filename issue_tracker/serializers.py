from django.forms import widgets
from rest_framework import serializers
from collaborate.issue_tracker.models import *



class IssueManagerSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField('get_issues')
    
    def get_issues(self, obj):
        issues = obj.get_issues()
        serialized_issues = []
        for i in issues:
            s = IssueSerializer(i)
            serialized_issues.append(s.data)
        return serialized_issues

    class Meta:
        model = IssueManager

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.name = attrs.get('name', instance.name)
            instance.description = attrs.get('description', instance.description)
            instance.account = attrs.get('account_id', instance.account)
        return IssueManager(**attrs)


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.name = attrs.get('name', instance.name)
            instance.problem = attrs.get('problem', instance.problem)
            instance.status = attrs.get('status', instance.status)
            instance.issue_type = attrs.get('issue_type', instance.issue_type)
            instance.owner = attrs.get('owner', instance.owner)
            instance.manager = attrs.get('manager', instance.manager)
            instance.tags = attrs.get('tags', instance.tags)
            
        attrs['comments'] = {}
        return Issue(**attrs)


