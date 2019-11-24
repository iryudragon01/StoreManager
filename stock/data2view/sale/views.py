from django.shortcuts import render,redirect
from stock.models import Sale
from stock.data2view.user import action,queries

def IndexView(request,url):
    if not action.is_worker_genius(request,url):
        return redirect('stock:index_store',url = request.session['url'])
    content = {}
    



    return render(request, 'stock/sale/index.html',content)