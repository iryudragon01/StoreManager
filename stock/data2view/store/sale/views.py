from django.shortcuts import render,redirect,Http404,HttpResponse
from stock.models import Sale,Item
from stock.data2view.user import action,queries
from . import forms,ajax
from django.db.models import Sum
from django.utils import timezone
import json

def IndexView(request,url):
    content = {}
    worker = queries.get_worker(url, username=request.session['worker'])
    if request.POST:
        if request.is_ajax():
            data = json.dumps(ajax.SaleEnableButton(request,worker))
            return HttpResponse(data,content_type='application/json')
    items = Item.objects.filter(
        user=worker.supervisor )

    form_list=[]
    if items.exists():
        content['items'] = items
        for item in items:
            form_list.append(salelist(request,item))
        content['forms'] = form_list
    else:
        content['message']   = 'you donot have any item'
    BTNDisplay= "Enable" if worker.enable_sale else "Disable"
    BTNclass= "btn-outline-success" if worker.enable_sale else "btn-outline-secondary"
    BTNValue =  1 if worker.enable_sale else 0
    EnableBTN={'label':BTNDisplay,'value':BTNValue,'class':BTNclass}
    content['enableBTN']=EnableBTN
    worker.save()
    return render(request, 'stock/store/sale/index.html',content)


def DetailView(request,url,pk):
    content = {}
    worker =queries.get_worker(url,request.session['worker'])
    item= Item.objects.get(id=pk)
    if item:
        sale_1 = Sale.objects.filter(
                    item=item,
                    creater_id=worker.id,
                    create_time__gt=worker.date_log,
                    create_time__lte=timezone.now()
                    )
        if sale_1:
            content['sales']=sale_1
        else:
            print('sale donot exists')


    return render(request,'stock/store/sale/detail.html',content)

def DeleteView(request,url,pk):
    sale = Sale.objects.filter(id=pk)
    item_id=sale[0].item.id
    if sale.exists():
        if sale[0].creater_id == queries.get_worker(url=request.session['url'],
                                    username=request.session['worker']).id:
            delsale = sale[0]
            delsale.delete()
    return redirect('stock:detail_sale',url=request.session['url'],pk=item_id)

def ListView(request,url):
    content = {}
    worker = queries.get_worker(url,username=request.session['worker'])
    sales = Sale.objects.filter(
        creater_id=worker.id,
        create_time__gt=worker.date_log
    )
    if sales.exists():
        content['sales']=sales
    else:
        content['message'] = 'no sale'
    return render(request,'stock/store/sale/list.html',content)


def AjaxSaleView(request,url):
    result={}
    if request.POST:
        if request.is_ajax():
            print('it ajax')
            worker = queries.get_worker(url,username=request.session['worker'])
            if not worker.enable_sale:
                return HttpResponse(json.dumps({'errors':'worker disable'}),content_type='application/json')
            name = request.POST.get('name') if 'name' in request.POST else ""
            methon = request.POST.get('value') if 'value' in request.POST else 'Unknow'
            item = Item.objects.get(name=name,
                                user=queries.get_user(url))
            sale = Sale(
                    item=item,
                    volume=1,
                    creater_id=worker.id,
                    create_time=timezone.now(),
                    editer_id=worker.id,
                    edit_time=timezone.now()

                )
            sale.save()
            result = salelist(request,item)
            #else:
            #    result = {'fail':'norecorded'}
            data = json.dumps(result)
            print(data)
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404
    else:
        raise Http404

def salelist(request,item):
    worker =queries.get_worker(
            url=request.session['url'],
            username=request.session['worker'])
    sale_1 = Sale.objects.filter(
                creater_id=worker.id,
                create_time__lt=worker.date_log
                )
    sale_2 = Sale.objects.filter(
                creater_id=worker.id
                )
    first = sale_1.aggregate(Sum('volume'))['volume__sum'] if sale_1.exists() else 0
    now   = sale_2.aggregate(Sum('volume'))['volume__sum'] if sale_2.exists() else 0
    print(sale_1.count(),' sale1 count',worker.id)
    return {
        'id':item.id,
        'name':item.name,
        'first':first,
        'now':now,
        'sale':(now-first)
    }
