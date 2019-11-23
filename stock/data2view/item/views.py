from django.shortcuts import render, redirect
from stock.models import Item,User,Worker
from . import forms
from stock.data2view.user import queries


def CreateView(request,url):
    if 'worker' not in request.session:
        print('no worker in session')
        return redirect('stock:index')
    user_req = User.objects.filter(email=request.user)
    if not user_req.exists():
        return redirect('stock:index')
    user_url = queries.get_user(url)
    if user_req[0] != user_url:
        return redirect('stock:index')

    content = {}
    form = forms.CreateItemForm()
    content['form'] = form
    return render(request, 'stock/item/create.html',content)
