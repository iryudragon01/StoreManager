from django.shortcuts import render, redirect, Http404
from stock.models import Sale, Item
from stock.data2view.user import action, queries
from datetime import datetime
from django.db.models import Sum


def IndexView(request, url):
    content = dict()
    worker = queries.get_worker(url, request.session['worker'])
    item_a = Item.objects.filter(
        type=1,
        user=worker.supervisor,
        is_active=1
    )
    item_b = Item.objects.filter(
        type=2,
        user=worker.supervisor,
        is_active=1
    )
    item_c = Item.objects.filter(
        type=3,
        user=worker.supervisor,
        is_active=1
    )
    sale = lambda item: sumSale(item, worker)
    if item_a.exists():
        content['nostocks'] = list(map(sale, item_a))
    if item_b.exists():
        content['airpays'] = list(map(sale, item_b))
    if item_a.exists():
        content['stocks'] = list(map(sale, item_c))

    return render(request, 'stock/store/summary/index.html', content)


def sumSale(item, worker):
    pre_sale = Sale.objects.filter(
        creater_id=worker.id,
        item=item,
        create_time__lt=worker.date_log
    )
    sales = Sale.objects.filter(
        creater_id=worker.id,
        item=item,
        create_time__gt=worker.date_log,
        create_time__lt=datetime.now()
    )
    volume = sales.aggregate(Sum('volume'))['volume__sum'] if sales.exists() else 0
    pre_volume = pre_sale.aggregate(Sum('volume'))['volume__sum'] if pre_sale.exists() else 0
    all_volume = volume + pre_volume
    result = {'name': item.name, 'volume': volume, 'pre_volume': pre_volume, 'all_volume': all_volume, 'sales': sales}
    sum = 0
    if sales.exists():
        for sale in sales:
            sum += sale.sale_price*sale.volume
    result['sum'] = sum
    return result