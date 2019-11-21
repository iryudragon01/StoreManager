from django.shortcuts import render,redirect
from stock.models import User,Worker
from . import forms
import hashlib,json
from stock.data2view.user import action
from django.contrib.auth import authenticate


def IndexView(request,url):
    context = {}
    return render(request, 'stock/store/index.html',context)


def ListView(request,url):
    content = {"title": url}
    supervisor = User.objects.filter(email=request.user)
    if supervisor.exists():
        workers = Worker.objects.filter(supervisor=supervisor[0])
        if workers.exists():
            content['workers'] = workers
            if workers.count() >= supervisor[0].under_worker:
                content['add_worker'] = 'worker exceed limit'
    return render(request, 'stock/store/list.html', content)


def WorkerCreateView(request, url):
    query = User.objects.filter(email=request.user.email)
    if not query.exists():
        return redirect('stock:login_user')
    user = query[0]
    worker = Worker.objects.filter(supervisor=user)
    if worker.exists():
        if worker.count() >= user.under_worker:
            return redirect('stock:index_store', url=user.url)

    form = forms.WorkerCreateForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            worker = Worker(
                supervisor=user,
                username=form.cleaned_data['username'],
                password=hashlib.sha512(
                    form.cleaned_data['password'].encode('utf-8')).hexdigest()
            )
            worker.save()
            return redirect('stock:list_worker', url=user.url)

    content = {'form': form}

    return render(request, 'stock/store/create_worker.html', content)


def WorkerLoginView(request, url):
    query = User.objects.filter(url=url)
    if not query.exists():
        redirect('stock:index')
    user = query[0]
    form = forms.WorkerLoginForm(request.POST or None)
    content = {
        'form': form,
        'parent': request.user
    }
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            worker = Worker.objects.filter(
                supervisor=user,
                username=username,
                password=hashlib.sha512(password.encode('utf-8')).hexdigest()
            )
            if worker.exists():
                track = action.update_track(request, 55)
                update = worker[0]
                update.track = track
                update.save()
                request.session['worker'] = update.username
                return redirect('stock:work')
                # response['Location'] += '?track='+track
                # return response
    return render(request, 'stock/user/login_worker.html', content)


def EditWorkerView(request,url, pk):
    query = User.objects.filter(url=url)
    if not query.exists():
        return redirect('stock:index')
    user = query[0]
    content = {}
    query = Worker.objects.filter(supervisor=user,id=pk)
    if not query.exists:
        return redirect('stock:index_store')
    worker = query[0]
    form = forms.EditWorkerForm(request.POST or None, instance=worker)
    if request.POST:
        if form.is_valid():
            if 'DELETE' in request.POST:
                user = authenticate(email=request.user, password=request.POST['verifypwd'])
                if user:
                    worker.delete()
                    return redirect('stock:list_worker',url=request.user.url)
                else:
                    content['message'] = 'cannot delete password wrong'
            else:
                worker.access_level = form.cleaned_data['access_level']
                worker.save()
                return redirect('stock:list_worker',url=request.user.url)
    content['form'] = form
    content['name'] = worker.username
    return render(request, 'stock/store/edit_worker.html', content)


def LogoutView(request):
    # request.session.remove()
    return redirect('stock:index')

