from django.http.response import HttpResponse
from .models import Question, Answers
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import answerForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,"mainpg/home.html",{'questions':Question.objects.all()})

class ask(LoginRequiredMixin,CreateView):
    model = Question
    fields = ['subject', 'desc']

    def form_valid(self, form):
        form.instance.author=self.request.user
        form.instance.likes = 0
        form.instance.dislikes = 0
        messages.success(self.request,'Your Question is now Posted')
        return super().form_valid(form)

@login_required()
def like(request,q_id):
    q = Question.objects.filter(id = q_id)[0]
    q.likes = q.likes + 1
    q.save()
    return redirect('home')


@login_required()
def dislike(request,**kwargs):
    Q = Question.objects.filter(id = kwargs['pk'])[0]
    Q.dislikes += 1
    Q.save()
    return redirect('home')


@login_required()
def answer(request, **kwargs):
    qsn = Question.objects.filter(id = kwargs['pk'])[0]
    if request.method == 'POST':
        form=answerForm(request.POST)
        if form.is_valid():
            form.instance.of = qsn
            form.instance.author = request.user
            form.save()
            messages.success(request," SUCCESSFULLY ANSWERED")
            return redirect('home')
    else:
        form = answerForm
    return render(request,'mainpg/answer.html',{'Form':form})


def viewans(request, **kwargs):
    qn = Question.objects.filter(id = kwargs['pk'])[0]
    try:
        qn.allans
    except:
        Answers.objects.create(of = qn)
    else:
        pass
    finally:
        return render(request, 'mainpg/allans.html',{'ans':qn.allans.all()})
