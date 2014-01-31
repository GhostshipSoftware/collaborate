from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



# Create your models here.

"""
Need to extend the User class, add a variable called account that
is a one to one relationship to an Account model which holds all the
needed info about an account.
"""


class BillingUser(AbstractUser):

    account = models.ForeignKey('Account', null=True)
    experience_made = models.IntegerField(null=True)
    experience_needed = models.IntegerField(null=True)
    level = models.IntegerField(null=True)     
    
    def award_experience(self, exp_to_award):
        self.experience_made += exp_to_award
        if self.experience_made == self.experience_needed:
            self.level()
        elif self.experience_made > self.experience_needed:
            offset = self.experience_made - self.experience_needed
            self.level(offset)
        self.save()

    def level(self, offset=None):
        if offset:
            self.experience_made = offset
        else:
            self.experience_made = 0
        self.experience_needed = self.experience_needed * 2
        self.save()

class Account(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    company_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    
    def __unicode__(self):
        return self.company_name

    def get_users(self):
        users = [ user for user in BillingUser.objects.all() if user.account_id == self.id ]
        return users
    

#class UserProfile(models.Model):
    
#    user = models.OneToOneField(User)
#    account = models.ForeignKey(Account, null=True)
#
#    def __str__(self):
 #       return "%s's profile" % self.user

#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        profile, created = UserProfile.objects.get_or_create(user=instance)
        
#post_save.connect(create_user_profile, sender=User)

#@receiver(post_save, sender=BillingUser)
#def create_auth_token(sender, instance=None, created=False, **kwargs):
#    if created:
#        Token.objects.create(user=instance) 
