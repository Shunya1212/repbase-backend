from django.db import models

class Animal(models.Model):
    code = models.CharField(max_length=512, help_text='animal code')