from django.shortcuts import render, redirect
from stock.models import User, Worker
from . import forms
import hashlib
from django.contrib.auth import authenticate
from stock.data2view.user import queries, action


def bootstrap(request):
    return render(request, 'stock/store/bootstrap.html')


def StoreSearchView(request):
    content = {}
    if request.POST:
        if 'search' in request.POST:
            search = request.POST['search']
            users = User.objects.all()
            list = []
            for user in users:
                print(search, '  ',user.url)
                if search in user.url:
                    list.append(user.url)
            if list:
                content['urls'] = list
            else:
                content['message'] = 'page not found'

    return render(request, 'stock/store/search.html',content)


def IndexView(request, url):
    context = {}
    if not queries.is_url_exists(url):  # check if url is exists
        return redirect('stock:index')
    if not request.user.is_authenticated:  # if not authenticated
        if 'worker' in request.session:
            if queries.is_session_match(
                    track=request.session['track'],
                    username=request.session['worker'],
                    url=url
            ):
                pass
            else:
                return redirect('stock:login_worker', url=url)

        else:
            return redirect('stock:login_worker', url=url)
    return render(request, 'stock/store/index.html', context)


def ListView(request, url):
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
    content = {}
    current_user = User.objects.filter(email=request.user.email)
    if not current_user.exists():
        return redirect('stock:login_user')
    user = current_user[0]
    worker = Worker.objects.filter(supervisor=user)
    if worker.exists():
        if worker.count() >= user.under_worker:
            return redirect('stock:index_store', url=user.url)

    form = forms.WorkerCreateForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            if not queries.is_worker_exists(url=url, username=form.cleaned_data['username']):
                action.create_worker(request, url,
                                     username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])
                return redirect('stock:list_worker', url=user.url)
            else:
                content['message'] = 'already exists'

    content['form'] = form

    return render(request, 'stock/store/create_worker.html', content)


def WorkerLoginView(request, url):
    action.clear_worker(request)
    content = {}
    if not queries.is_url_exists(url=url):
        redirect('stock:index')
    user = queries.get_user(url=url)
    form = forms.WorkerLoginForm(request.POST or None)
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
                action.set_worker(request,url,worker[0].username)
                return redirect('stock:display_sum', url=url)
            else:
                content['message'] = 'use or password not correct'
                # response['Location'] += '?track='+track
                # return response
    content['form'] = form
    return render(request, 'stock/store/login_worker.html', content)


def EditWorkerView(request, url, pk):
    content = {}
    if not request.user.is_authenticated:
        if not queries.is_url_exists(url=url):
            return redirect('stock:index')
        user = queries.get_user(url)
        if user.emal != user.email:
            return redirect('stock:index')
    if not queries.is_worker_exists(url=url, pk=pk):
        return redirect('stock:list_worker', url=url)
    worker = queries.get_worker(url=url, pk=pk)
    form = forms.EditWorkerForm(request.POST or None, instance=worker)
    if request.POST:
        if form.is_valid():
            if 'DELETE' in request.POST:
                user = authenticate(email=request.user, password=request.POST['verifypwd'])
                if user:
                    worker.delete()
                    return redirect('stock:list_worker', url=request.user.url)
                else:
                    content['message'] = 'cannot delete password wrong'
            else:
                worker.access_level = form.cleaned_data['access_level']
                worker.save()
                return redirect('stock:list_worker', url=request.user.url)
    content['form'] = form
    content['value'] = worker.access_level
    return render(request, 'stock/store/edit_worker.html', content)


def LogoutWorkerView(request, url):
    action.clear_worker(request)
    return redirect('stock:index_store', url=url)


def SumView(request, url):
    return render(request, 'stock/store/display/sum.html')
