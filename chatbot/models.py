# -*- coding: utf-8 -*-
import datetime
import urllib
from django.db import models
from django.utils.timezone import now
from django.core.files import File
import os


# Create your models here.
class Chat(models.Model):
    id=models.AutoField(primary_key=True)
    chat_user=models.CharField(blank=True,max_length=255)
    chat_text=models.TextField()
    chat_wrong_intent=models.CharField(blank=True,max_length=256)
    chat_isCorrect=models.BooleanField(default=False)
    chat_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.chat_text




