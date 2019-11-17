from django.shortcuts import render,redirect
from . import forms,action
from stock.models import User

def CreateView(request):
    form = forms.RegisterForm(request.POST or None)
    content = {}
    message = 'create new user'
    if request.POST:
        if form.is_valid():
            message = 'success'
    content['form'] = form
    content['message'] = message
    return render(request,'stock/user/create.html',content)


def LoginView(request):
    form = forms.LoginForm(request.POST or None)
    content = {
        'form': form
    }
    if form.is_valid():
        content['message'] = 'success'
    return render(request,'stock/user/login.html',content)


def WorkerView(request,owner):
    if User.objects.filter(username=owner).count() == 0:
        return redirect('stock:create_user')
    content = {}
    form = forms.WorkerForm(request.POST or None)
    content['form'] = form

    return render(request,'stock/user/worker.html',content)