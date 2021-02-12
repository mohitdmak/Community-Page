from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from allauth.socialaccount.models import SocialAccount

class Question(models.Model):
    subject = models.CharField(max_length = 200)
    desc = models.TextField()
    time = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "Question")
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    def __str__(self):
        return self.subject
    def get_absolute_url(self):
        return reverse('home')

class Answers(models.Model):
    ans = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='ansrs')
    time = models.DateTimeField(default=timezone.now)
    of = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='allans')

class Like(models.Model):
    ofQ = models.ForeignKey(Question, on_delete = models.CASCADE, related_name = 'liked')
    byU = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'saved')
    def __str__(self):
        return str(self.byU.id)

class DisLike(models.Model):
    ofQ = models.ForeignKey(Question, on_delete = models.CASCADE, related_name = 'disliked')
    byU = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'dissaved')
    def __str__(self):
        return str(self.byU.id)

class Profile(models.Model):
    usr = models.OneToOneField(SocialAccount, on_delete = models.CASCADE, related_name = 'profile')
    Name = models.CharField(max_length = 100)
    Contact_Email = models.EmailField()
    dp = models.ImageField(upload_to = 'profilepics')
    Bio = models.TextField()
    originaldp = models.CharField(max_length = 9999, default="")
    
