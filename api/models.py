from django.db import models

# Create your models here.

class Application(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    application_name = models.CharField(max_length=100)
    enabled = models.BooleanField()
    

    def __unicode__(self):
        return self.application_name
