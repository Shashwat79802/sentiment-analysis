from django.db import models


class User(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
