from django.contrib import admin
from django.urls import path
from . import views as mainpgviews

urlpatterns = [
    path('', mainpgviews.home)
]