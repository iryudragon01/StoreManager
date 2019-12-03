from django.shortcuts import render, redirect, Http404
from stock.models import Item, User, Worker, Stock, Sale
from . import forms, scripts
from stock.data2view.user import queries, action
from datetime import datetime
from django.db.models import Sum


def CreateView(request, url):
    content = {}
    instance = Item(user=queries.get_user(url))
    form = forms.CreateItemForm(request.POST or None, instance=instance)
    if request.POST:
        if form.is_valid():
            if scripts.is_item_exists(url, name=form.cleaned_data['name']):
                content['message'] = 'item already exist'
            else:
                form.save()
                content['message'] = 'item save'
                form = forms.CreateItemForm()
        else:
            content['message'] = 'form is not valid'

    content['form'] = form
    return render(request, 'stock/store/item/create.html', content)


def EditView(request, url, pk):
    if not action.is_worker_genius(request, url, access_level=1):
        return redirect('stock:index_store', url=url)
    if not scripts.is_item_exists(url, id=pk):
        return redirect('stock:index_store', url=url)
    item = Item.objects.get(id=pk, user=queries.get_user(url))
    content = {}
    content['item'] = item
    form = forms.EditItemform(request.POST or None, instance=item)
    if request.POST:
        if form.is_valid():
            if 'DELETE' in request.POST:
                worker = queries.get_worker(url, request.session['worker'])
                if action.hash_pwd(request.POST['verifypwd']) == worker.password:
                    item.delete()
                    return redirect('stock:list_item', url=url)
                else:
                    content['message'] = 'password incorrect item not delete'
            else:
                form.save()
                return redirect('stock:list_item', url)

    content['form'] = form
    return render(request, 'stock/store/item/edit.html', content)


def ListView(request, url):
    if not action.is_worker_genius(request, url, access_level=1):
        return redirect('stock:index_store', url=url)
    content = {}
    items = Item.objects.filter(user=queries.get_user(url))
    content['items'] = items
    return render(request, 'stock/store/item/list.html', content)


def is_admin_level(function_run):
    def wrapper(request, *args, **kwargs):
        worker = queries.get_worker(url=request.session['url'], username=request.session['worker'])
        if worker.access_level == 1:
            return function_run(request, *args, **kwargs)
        else:
            raise Http404('must be admin level worker')

    return wrapper


@is_admin_level
def TopupView(request, url):
    content = {}
    items = Item.objects.filter(
        user=queries.get_user(url),
        is_active=True,
        type=3
    )
    worker = queries.get_worker(url, request.session['worker'])
    if request.POST:
        for item in items:  # ['item', 'volume', 'creater_id', 'create_time', 'editer_id', 'edit_time']
            stock = Stock(
                item=item,
                volume=int(request.POST[item.name]),
                user=worker.supervisor.email,
                creater_id=worker.id,
                create_time=datetime.now(),
                editer_id=worker.id,
                edit_time=datetime.now()
            )
            if stock.volume > 0:
                stock.save()
        return redirect('stock:list_topup', url=url)
    content['items'] = items
    return render(request, 'stock/store/item/topup.html', content)


@is_admin_level
def ListTopupView(request, url):
    content = {}
    worker = queries.get_worker(url, request.session['worker'])
    content['topups'] = Stock.objects.filter(
        user=worker.supervisor.email,
        create_time__gt=worker.date_log
    )
    return render(request, 'stock/store/item/list_topup.html', content)


@is_admin_level
def StockView(request, url):
    content = {}
    worker = queries.get_worker(url, request.session['worker'])
    items = Item.objects.filter(
        user=queries.get_user(url),
        is_active=True,
        type=3
    )
    sum = lambda item:sumstock(request,item)
    content['stocks'] = list(map(sum, items))
    return render(request, 'stock/store/item/stock.html', content)


def sumstock(request, item):
    content = {'name': item.name}
    stock = Stock.objects.filter(
        user=request.session['email'],
        item=item
    ).aggregate(Sum('volume'))['volume__sum'] if Stock.objects.filter(
        user=request.session['email'],
        item=item
    ).exists() else 0
    sale = Sale.objects.filter(
        user=request.session['email'],
        item=item
    ).aggregate(Sum('volume'))['volume__sum'] if Sale.objects.filter(
        user=request.session['email'],
        item=item
    ).exists() else 0
    content['sum'] = stock - sale
    return content
