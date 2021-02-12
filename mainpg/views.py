from django.http.response import HttpResponse
from .models import Question, Answers, Like, DisLike, Profile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import answerForm, UserPicUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount

def home(request):
    if request.user.is_authenticated:
        u = request.user
        usr = SocialAccount.objects.filter(user = u)[0]
        pic = usr.extra_data['picture']
        for q in Question.objects.all():
            q.likes = q.liked.count()
            q.dislikes = q.disliked.count()
            q.save()
        qset = Question.objects.all().order_by('-likes')
        a = qset.count()
        return render(request,"mainpg/base.html",{'questions':qset, 'pic':pic,'total':a})
    for q in Question.objects.all():
        q.likes = q.liked.count()
        q.dislikes = q.disliked.count()
        q.save()
    qset = Question.objects.all().order_by('-likes')
    a = qset.count()
    return render(request,"mainpg/home.html",{'questions': qset,'total':a})

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
    u = request.user
    for x in q.liked.all():
        if str(u.id) == str(x):
            messages.success(request,'Your have already upvoted the Question')

            return redirect('home')
    for x in q.disliked.all():
        if str(u.id) == str(x):
            messages.success(request,'Your have upvoted the previously downvoted Question !')
            x.delete()
            Like.objects.create(byU = u, ofQ = q)
            q.save()
            return redirect('home')
    Like.objects.create(byU = u, ofQ = q)
    q.save()
    messages.success(request,'Your have upvoted the Question !!!')
    return redirect('home')


@login_required()
def dislike(request,q_id):
    q = Question.objects.filter(id = q_id)[0]
    u = request.user
    for x in q.disliked.all():
        if str(u.id) == str(x):
            messages.success(request,'Your have already downvoted the Question')
            return redirect('home')
    for x in q.liked.all():
        if str(u.id) == str(x):
            messages.success(request,'Your have downvoted the previously upvoted Question')
            x.delete()
            DisLike.objects.create(byU = u, ofQ = q)
            q.save()
            return redirect('home')
    DisLike.objects.create(byU = u, ofQ = q)
    q.save()
    messages.success(request,'Your have downvoted the Question !!!')
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

def seeprofile(request, **kwargs):
    u = User.objects.filter(id = kwargs['pk'])[0]
    su = SocialAccount.objects.filter(user = u)[0]
    suname = su.extra_data['name']
    suemail = su.extra_data['email']
    suoriginaldp = su.extra_data['picture']
    qset = Question.objects.filter(author = u)
    rec = qset[0]
    recentq = rec.id
    recent = rec.subject[0:24]

    try:
        su.profile
    except:
        Profile.objects.create(usr = su, Name = suname, Contact_Email = suemail, Bio = "Hey There! I am using the BITS Community Page!", originaldp = suoriginaldp)
        Profile.save()
        p = Profile.objects.filter(usr = su)[0]
    else:
        p = Profile.objects.filter(usr = su)[0]
    finally:
        if request.user == su:
            if request.method=='POST':
                u_form=UserUpdateForm(request.POST,instance=request.user)
                p_form=UserPicUpdateForm(request.POST,request.FILES,instance=request.user.profile)
                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    p_form.save()
                    usernamee = u_form.cleaned_data.get('name')
                    messages.success(request,f'CONGRATS {usernamee} !, YOUR PROFILE INFO IS UPDATED!')
                    return redirect("home")
            else:
                u_form=UserUpdateForm(instance=request.user.profile)
                p_form=UserPicUpdateForm(instance=request.user.profile)
                context={'u_form':u_form,'p_form':p_form}
                return render(request,'mainpg/profile.html',context)
            p = Profile.objects.filter(usr = su)[0]
            return render(request, 'mainpg/profile.html', {'profile': p})
        else:
            p = Profile.objects.filter(usr = su)[0]
            x = "https://www.google.com/search?q=" + str(p.Contact_Email)
            return render(request, 'mainpg/seeprofile.html', {'profile': p, 'picc': x, 'recent': recent, 'recentq':recentq})