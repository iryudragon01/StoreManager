from django.shortcuts import render, redirect
from . import forms, action
from stock.models import User, Worker
from django.contrib.auth import authenticate, login, logout
import hashlib


def CreateView(request):
    form = forms.RegisterForm(request.POST or None)
    content = {}
    if request.POST:
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            url = form.cleaned_data['url']
            form.save()
            user = authenticate(email=email, password=password)
            login(request, user)
            request.session['supervisor'] = user.email
            action.create_worker(request, url, username='admin', password=password)
            action.set_worker(request,url,'admin')
            return redirect('stock:index_store', url=user.url)
    content['form'] = form
    return render(request, 'stock/user/create.html', content)


def LoginView(request):
    form = forms.LoginForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                request.session['supervisor'] = user.email
                action.set_worker(request,user.url,'admin')
                return redirect('stock:index_store', url=user.url)

    content = {'form': form}

    return render(request, 'stock/user/login.html', content)


def LogoutView(request):
    url = request.session['url']
    action.clear_worker(request)
    logout(request)
    return redirect('stock:index_store', url=url)
