from django.shortcuts import render,redirect
from . import forms,action



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