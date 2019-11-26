from django.shortcuts import render,redirect,Http404,HttpResponse
from stock.models import Sale,Item
from stock.data2view.user import action,queries
from . import forms,ajax
from django.db.models import Sum
from django.utils import timezone
import json

def IndexView(request,url):
    if not action.is_worker_genius(request,url):
        return redirect('stock:index_store',url = request.session['url'])
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
            form_list.append(salelist(request,item,url))  
        content['forms'] = form_list
    else:
        content['message']   = 'you donot have any item'    
    worker.enable_sale=False
    worker.save()    
    return render(request, 'stock/store/sale/index.html',content)

def ListView(request,url):
    if not action.is_worker_genius(request,url):
        return redirect('stock:index')
    content = {}        
    if request.POST:
        print('post')    
    else:
        print('get')    
    worker = queries.get_worker(url,username=request.session['worker'])    
    sales = Sale.objects.filter(
        user=worker.supervisor,
        create_worker=worker.username,
        create_time__gt=worker.date_log
    )
    if sales.exists():
        content['sales']=sales
    else:
        content['message'] = 'no sale'    
    return render(request,'stock/store/sale/list.html',content)


def AjaxSaleView(request,url):   
    if request.POST:        
        if request.is_ajax(): 
            if not action.is_worker_genius(request,url):
                raise Http404
            worker = queries.get_worker(url,username=request.session['worker'])
            if not worker.enable_sale:
                return HttpResponse(json.dumps({'errors':'worker disable'}),content_type='application/json')
            name = request.POST.get('name') or 'no name data'
            value = request.POST.get('value') or 'no value data'
            items = Item.objects.filter(name=name)
            if items.exists():
                sale = Sale(
                    item=items[0],
                    volume=1,
                    user=queries.get_user(url).email,
                    create_worker=queries.get_worker(url,username=request.session['worker']),
                    create_time=timezone.now(),
                    edit_worker=queries.get_worker(url,username=request.session['worker']),
                    edit_time=timezone.now()

                )
                sale.save()                
                result = salelist(request,items[0],url)
            else:
                result = {'fail':'norecorded'}  
            data = json.dumps(result)
            print(data)
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404
    else:
        raise Http404    

def salelist(request,item,url):
    first=0
    now=0
    sale=0    
    worker =queries.get_worker(url,request.session['worker'])
    sale_1 = Sale.objects.filter(
                item=item,
                create_worker=worker.username,
                create_time__lt=worker.date_log
                )
    sale_2 = Sale.objects.filter(
                item=item,
                create_worker=worker.username,
                create_time__lt=timezone.now()
                )
    if sale_1.exists():
        first=  sale_1.aggregate(Sum('volume'))['volume__sum']  
    if sale_2.exists():
        now=  sale_2.aggregate(Sum('volume'))['volume__sum'] 
    sale=now-first   
    return {
        'name':item.name,
        'first':first,
        'now':now,
        'sale':sale
    }
        