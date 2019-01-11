from django.db import models

 # Create Movie Model
class Shorturl(models.Model):
    url = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    short = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True) # When it was create
    updated_at = models.DateTimeField(auto_now=True) # When i was update
    creator = models.ForeignKey('auth.User', related_name='shorturl', on_delete=models.CASCADE)
