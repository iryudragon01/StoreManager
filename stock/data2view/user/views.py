from django.shortcuts import render,redirect
from . import forms,action
from stock.models import User
from django.contrib.auth import authenticate,login,logout


def IndexView(request):
    return render(request,'stock/index/index.html')


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
            login(request,user)
            return redirect('stock:index')
    content['form'] = form
    content['message'] = message
    return render(request,'stock/user/create.html',content)


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
            return redirect('stock:index')
    return render(request,'stock/user/login.html',content)


def LogoutView(request):
    logout(request)
    return redirect('stock:index')


def WorkerView(request,owner):
    if User.objects.filter(username=owner).count() == 0:
        return redirect('stock:create_user')
    content = {}
    form = forms.WorkerForm(request.POST or None)
    content['form'] = form

    return render(request,'stock/user/worker.html',content)