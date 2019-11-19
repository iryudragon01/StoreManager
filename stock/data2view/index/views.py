from django.shortcuts import redirect, render,HttpResponse,Http404
from stock.models import Worker
import string
import random
import json


def IndexView(request):
    return render(request,'stock/index/index.html')


def AjaxView(request):
    if request.POST:
        name = request.POST.get('name') or 'no name data'
        value = request.POST.get('value') or 'no value data'
        print('name:', name, 'value:', value)
        result = ['recorded',name,value]
        data = json.dumps(result)
        return HttpResponse(data, content_type='application/json')

    if request.is_ajax():
        list = ['iryu dragon', 'narisa wahkor', 'padthai shrimp ']
        data = json.dumps(list)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def WorkView(request):
    content = {}
    if 'worker' in request.session:
        content['worker']= request.session['worker']
    else:
        return redirect('stock:login_worker')
    if request.GET:
        worker = Worker.objects.filter(track=request.session['track'])
        if worker.exists():
            newtrack = update_track(request, 55)
            update = worker[0]
            update.track = newtrack
            update.save()
        else:
            request.session['worker'] = None
            return redirect('stock:login_worker')
    if request.POST:
        print(request.session['worker'], ' post post')
    print(request.session['worker'], ' pre post')
    return render(request, 'stock/index/index.html',content)


def update_track(request, length=55):
    letters = string.ascii_lowercase
    newtrack = ''.join(random.choice(letters) for i in range(length))
    request.session['track'] = newtrack
    return newtrack
