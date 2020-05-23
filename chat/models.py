from django.db import models
from django.conf import settings
# Create your models here.

class UserAndEncodingDetail(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    encoding=models.TextField()
    person_name=models.CharField(max_length=20,default='admin')

    def __str__(self):
        return self.person_name