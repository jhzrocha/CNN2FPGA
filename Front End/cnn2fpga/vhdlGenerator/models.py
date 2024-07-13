from django.db import models
from django.contrib.auth.models import User

class Expression(models.Model):
    ds_expression_ptbr = models.CharField(max_length=250)
    ds_expression_en = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1)
