from django.forms import widgets
from rest_framework import serializers
from billing.models import *

class AccountSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField('get_users')
    class Meta:
        model = Account
   
    def get_users(self, obj):
        users = obj.get_users()
        return users

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.company_name = attrs.get('company_name', instance.company_name)
            return instance
        return Account(**attrs)

class UserSerializer(serializers.ModelSerializer):
    account_id = serializers.SerializerMethodField('get_account_id')
    password = serializers.CharField(required=False)
     
    class Meta:
        model = BillingUser
        fields = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'first_name', 'last_name', 'password', 'account_id')

    def get_account_id(self, obj):
        account_id = obj.account_id
        return account_id

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.id = attrs.get('id', instance.id)
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.email = attrs.get('email', instance.email)
            instance.username = attrs.get('username', instance.username)
            instance.is_active = attrs.get('is_active', instance.is_active)
            instance.is_staff = attrs.get('is_staff', instance.is_staff)
            instance.is_superuser = attrs.get('is_superuser', instance.is_superuser)
            if attrs.get('password') is None:
                instance.password = attrs.get('password', instance.password)
            else:
                instance.password = attrs.get('password')
                instance.set_password(instance.password)
            instance.account_id = attrs.get('account_id', instance.account_id)
            return instance
        user = BillingUser(**attrs)
        user.set_password(attrs['password'])
        return user
 

    
