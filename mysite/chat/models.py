from django.db import models

# Create your models here.

class UserAndEncodingDetail(models.Model):

    encoding=models.TextField()
    person_name=models.CharField(max_length=20,default='admin')

    def __str__(self):
        return self.person_name