from .models import Question,Like,DisLike
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
    ordering = ['-time']

    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request,'Your Question is now Posted')
        return super().form_valid(form)

def like(request,**kwargs):
    q = Question.objects.filter(id = kwargs['pk'])[0]
    try:
        q.liked
    except:
        Like.objects.create(oQ = q)
    else:
        pass
    finally:
        q.liked.num += 1
    return redirect('home')


def dislike(request, **kwargs):
    Q = Question.objects.filter(id = kwargs['pk'])[0]
    try:
        Q.disliked
    except:
        DisLike.objects.create(oQd = Q)
    else:
        pass
    finally:
        Q.disliked.numd += 1
    return redirect('home')
