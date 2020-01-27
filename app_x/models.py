from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from project_x.settings import BASE_DIR

# Create your models here.
class Records(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    Image=models.FileField(upload_to=BASE_DIR+'/pic',blank=True)
    eth_add=models.CharField(max_length=100,null=True)
    eth_private_key=models.CharField(max_length=50, null=True)
    residence = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    education = models.CharField(max_length=150, null=True)
    occupation = models.CharField(max_length=150, null=True)
    marital_status = models.CharField(max_length=50, null=True)
    bio = models.TextField()
    recorded_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.first_name
    class Meta:
        verbose_name_plural = "Records"
