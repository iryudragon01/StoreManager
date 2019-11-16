
from django.shortcuts import render,redirect
from django.contrib import auth
# Create your views here.


def indexView(request):
    return redirect('stock:create_user')