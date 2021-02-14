from django.http.response import HttpResponse
from .models import Question, Answers, Like, DisLike, Profile, FollowList
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
        su = SocialAccount.objects.filter(user = u)[0]
        suname = su.extra_data['name']
        suemail = su.extra_data['email']
        suoriginaldp = su.extra_data['picture']
        try:
            su.profile
        except:
            Profile.objects.create(usr = su, Name = suname, Contact_Email = suemail, Bio = "Hey There! I am using the BITS Community Page!", originaldp = suoriginaldp)
            p = Profile.objects.filter(usr = su)[0]
            p.save()
            
        else:
            p = Profile.objects.filter(usr = su)[0]
        
        if p.dp == 'default.png':
            pic = su.extra_data['picture']
        else:
            pic = p.dp.url
        for q in Question.objects.all():
            q.likes = q.liked.count()
            q.dislikes = q.disliked.count()
            q.save()
        qset = Question.objects.all().order_by('-likes')
        a = qset.count()
        return render(request,"mainpg/home.html",{'questions':qset, 'pic':pic,'total':a})
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

def feed(request):
    return render(request, 'mainpg/feed.html', {'feed': request.user.saved.all()})

@login_required()
def answer(request, **kwargs):
    qsn = Question.objects.filter(id = kwargs['pk'])[0]
    if request.user.is_authenticated:
        u = request.user
        usrr = SocialAccount.objects.filter(user = u)[0]
        p = Profile.objects.filter(usr = usrr)[0]
        if p.dp == 'default.png':
            pic = usrr.extra_data['picture']
        else:
            pic = p.dp.url
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
    return render(request,'mainpg/answer.html',{'Form':form, 'pic':pic})


def viewans(request, **kwargs):
    qn = Question.objects.filter(id = kwargs['pk'])[0]
    if request.user.is_authenticated:
        u = request.user
        usrr = SocialAccount.objects.filter(user = u)[0]
        p = Profile.objects.filter(usr = usrr)[0]
        if p.dp == 'default.png':
            pic = usrr.extra_data['picture']
        else:
            pic = p.dp.url
    
    try:
        qn.allans
    except:
        Answers.objects.create(of = qn)
    else:
        pass
    finally:
        return render(request, 'mainpg/allans.html',{'ans':qn.allans.all(), 'pic':pic})

def edit(request, **kwargs):
    u = User.objects.filter(id = kwargs['pk'])[0]
    su = SocialAccount.objects.filter(user = u)[0]
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST,instance=su.profile)
        if u_form.is_valid():
                u_form.save()
                usernamee = u_form.cleaned_data.get('Name')
                messages.success(request,f'CONGRATS {usernamee} !, YOUR PROFILE INFO IS UPDATED!')
                return redirect("home")
    else:
        u_form=UserUpdateForm(instance=su.profile)
        context={'u_form':u_form}
        return render(request, 'mainpg/profile.html', {'profile': su.profile,'u_form': u_form})

def editpic(request, **kwargs):
    u = User.objects.filter(id = kwargs['pk'])[0]
    su = SocialAccount.objects.filter(user = u)[0]
    p = Profile.objects.filter(usr = su)[0]
    if p.dp == 'default.png': 
        x = su.extra_data['picture']
    else:
        x = p.dp.url
    if request.method=='POST':
        p_form=UserPicUpdateForm(request.POST, request.FILES, instance=su.profile)
        if p_form.is_valid():
            p_form.save()
            usernamee = su.profile.Name
            messages.success(request,f'CONGRATS {usernamee} !, YOUR PROFILE INFO IS UPDATED!')
            return redirect("home")
    else:
        p_form=UserPicUpdateForm(instance=su.profile)
        return render(request, 'mainpg/profilepic.html', {'profile': su.profile, 'p_form': p_form, 'picc': x})

def seeprofile(request, **kwargs):
    u = User.objects.filter(id = kwargs['pk'])[0]
    su = SocialAccount.objects.filter(user = u)[0]
    suname = su.extra_data['name']
    suemail = su.extra_data['email']
    suoriginaldp = su.extra_data['picture']
    
    
    try:
        su.profile
    except:
        Profile.objects.create(usr = su, Name = suname, Contact_Email = suemail, Bio = "Hey There! I am using the BITS Community Page!", originaldp = suoriginaldp)
        Profile.save()
        p = Profile.objects.filter(usr = su)[0]
    else:
        p = Profile.objects.filter(usr = su)[0]
    finally:
        if request.user == su.user:
            qset = Question.objects.filter(author = u)
            if qset:
                rec = qset[0]
                recentq = rec.id
                recent = rec.subject[0:24]
                p = Profile.objects.filter(usr = su)[0]
                id = p.usr.user.id
                if p.dp == 'default.png': 
                    x = su.extra_data['picture']
                else:
                    x = p.dp.url 
                return render(request, 'mainpg/yourprofile.html', {'profile': p, 'picc': x, 'recent': recent, 'recentq':recentq, 'id': id})
            else:
                p = Profile.objects.filter(usr = su)[0]
                id = p.usr.user.id
                if p.dp == 'default.png': 
                    x = su.extra_data['picture']
                else:
                    x = p.dp.url 
                return render(request, 'mainpg/yourprofilenew.html', {'profile': p, 'picc': x,'id': id})
        else:
            p = Profile.objects.filter(usr = su)[0]
            us = SocialAccount.objects.filter(user = request.user)[0]
            qset = Question.objects.filter(author = u)
            if qset:
                rec = qset[0]
                recentq = rec.id
                recent = rec.subject[0:24]
                for x in us.followings.all():
                    if su == x.usrtf:
                        if p.dp == 'default.png':
                            x = su.extra_data['picture']
                        else:
                            x = p.dp.url
                    return render(request, 'mainpg/seeprofile2.html', {'profile': p, 'picc': x,'recent': recent, 'recentq':recentq })
                if p.dp == 'default.png':
                    x = su.extra_data['picture']
                else:
                    x = p.dp.url 
                return render(request, 'mainpg/seeprofile.html', {'profile': p, 'picc': x,'recent': recent, 'recentq':recentq })
            else:
                for x in us.followings.all():
                    if su == x.usrtf:
                        if p.dp == 'default.png':
                            x = su.extra_data['picture']
                        else:
                            x = p.dp.url
                    return render(request, 'mainpg/seeprofile2.html', {'profile': p, 'picc': x })
                if p.dp == 'default.png':
                    x = su.extra_data['picture']
                else:
                    x = p.dp.url 
                return render(request, 'mainpg/seeprofile.html', {'profile': p, 'picc': x})



def follow(request,**kwargs):
    u = User.objects.filter(id = kwargs['pk'])[0]
    usertofollow = SocialAccount.objects.filter(user = u)[0]
    username = usertofollow.extra_data['name']
    messages.success(request,f'You are now following { username } :)')
    su = SocialAccount.objects.filter(user = request.user)[0]
    su.followings.create(usrtf = usertofollow)
    return redirect("home")


def unfollow(request,**kwargs):
    u = User.objects.filter(id = kwargs['pk'])[0]
    usertoremove = SocialAccount.objects.filter(user = u)[0]
    su = SocialAccount.objects.filter(user = request.user)[0]
    username = usertoremove.extra_data['name']
    for fl in su.followings.all():
        if fl.usrtf == usertoremove:
            fl.delete()
    messages.success(request,f'You have successfully unfollowed { username } :(')
    return redirect('home')


def followinglist(request):
    su = SocialAccount.objects.filter(user = request.user)[0]
    return render(request,"mainpg/followinglist.html",{'flist': su.followings.all()})