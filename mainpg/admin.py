from django.contrib import admin
from .models import Profile, Question, Answers, Like, DisLike

admin.site.register(Question)
admin.site.register(Answers)
admin.site.register(Like)
admin.site.register(DisLike)
admin.site.register(Profile)
