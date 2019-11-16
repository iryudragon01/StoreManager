from django.shortcuts import render,redirect
from stock.models import Item


def CreateView(request):
    form = Item()
    return render(request,'stock/item/create.html',{'form',form})
