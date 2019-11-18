from django.shortcuts import render, redirect
from . import forms
from stock.models import User,Worker
from django.contrib.auth import authenticate, login, logout
import hashlib
import random
import string

def IndexView(request):
    return render(request, 'stock/user/index.html')


def CreateView(request):
    form = forms.RegisterForm(request.POST or None)
    content = {}
    message = 'create new user'
    if request.POST:
        if form.is_valid():
            form.save()
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('stock:index_user')
    content['form'] = form
    content['message'] = message
    return render(request, 'stock/user/create.html', content)


def LoginView(request):
    form = forms.LoginForm(request.POST or None)
    content = {
        'form': form
    }
    if request.POST:
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('stock:index_user')
    return render(request, 'stock/user/login.html', content)


def LogoutView(request):
    logout(request)
    return redirect('stock:index')


def WorkerView(request):
    user = User.objects.filter(email=request.user.email)
    if not user.exists():
        return redirect('stock:login_user')

    form = forms.WorkerForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            worker = Worker(
                supervisor=user[0],
                username=form.cleaned_data['username'],
                password=hashlib.sha512(
                         form.cleaned_data['password'].encode('utf-8')).hexdigest()
            )
            worker.save()

    content = {'form': form}

    return render(request, 'stock/user/worker.html', content)


def WorkerLoginView(request):
    form = forms.WorkerLoginForm(request.POST or None)
    content = {
        'form': form,
        'parent': request.user
    }
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            worker = Worker.objects.filter(
                username=username,
                password=hashlib.sha512(password.encode('utf-8')).hexdigest()
            )
            if worker.exists():
                track = random_track(55)
                update = worker[0]
                update.track = track
                update.save()
                response = redirect('stock:work')
                response['Location'] += '?track='+track
                return response
    return render(request, 'stock/user/workerlogin.html', content)


def WorkView(request):
    track = request.GET['track']
    worker = Worker.objects.filter(track=track)
    content = {}
    if worker.exists():
        newtrack = random_track()
        update = worker[0]
        update.track = newtrack
        update.save()
        content['track'] = newtrack
    return render(request, 'stock/user/work.html',content)


def random_track(length=55):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
