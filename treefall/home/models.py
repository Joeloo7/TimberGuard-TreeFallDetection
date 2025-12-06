from django.db import models
class usruploads(models.Model):
    flnm=models.FileField(upload_to='images')
    