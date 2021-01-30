from .models import Question
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    return render(request,"mainpg/home.html",{'questions':Question.objects.all()})

class ask(CreateView):
    model = Question
    fields = ['subject', 'desc']

    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request,'Your Question is now Posted')
        return super().form_valid(form)

def like(request,q_id):
    q = Question.objects.filter(id = q_id)[0]
    q.likes += 1
    return redirect('home')

def dislike(request,**kwargs):
    Q = Question.objects.filter(id = kwargs['pk'])[0]
    Q.dislikes += 1
    return redirect('home')