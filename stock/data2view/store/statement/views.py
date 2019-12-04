from django.shortcuts import render,redirect,Http404,HttpResponse
from stock.data2view.user import action,queries
from stock.models import Statement,Worker
from datetime import datetime


def createView(request, url, mode):
    content = {'mode': mode}
    worker = queries.get_worker(url,request.session['worker'])
    if request.POST and 'name' in request.POST:
        statement = Statement(
            user=queries.get_user(url),
            name=request.POST['name'],
            volume=int(request.POST['volume']),
            type=request.POST['mode'],
            creater_id=worker.id,
            create_time=datetime.now(),
            editer_id=worker.id,
            edit_time=datetime.now()
        )
        if statement.name and statement.volume > 0:
            statement.save()
            content['message'] = f'{statement.name} {statement.volume} saved'
        else:
            content['statement'] = statement
            content['message'] = 'form do not valid'

    return render(request, 'stock/store/statement/create.html', content)


def listView(request, url, mode):
    content = {'mode': mode}
    worker = queries.get_worker(url, request.session['worker'])
    content['workers'] = Worker.objects.filter(supervisor=worker.supervisor)
    statement = Statement.objects.filter(
        user=worker.supervisor,
        create_time__gt=worker.date_log,
        type=mode
    )
    if statement.exists():
        content['statements']= statement
    else:
        content['message'] = f'{mode} not found'

    return render(request, 'stock/store/statement/list.html', content)