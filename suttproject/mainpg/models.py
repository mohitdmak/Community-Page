from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.urls import reverse

class Question(models.Model):
    subject = models.CharField(max_length = 200)
    desc = models.TextField()
    time = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "Question")
    def __str__(self):
        return self.subject
    def get_absolute_url(self):
        return reverse('home')

class Like(models.Model):
    num = models.IntegerField()
    oQ = models.OneToOneField(Question,on_delete=models.CASCADE,related_name='liked')

class DisLike(models.Model):
    numd = models.IntegerField()
    oQd = models.OneToOneField(Question,on_delete=models.CASCADE,related_name='disliked')