from django.shortcuts import render, redirect
from . import forms, action
from stock.models import User, Worker
from django.contrib.auth import authenticate, login, logout
import hashlib


def ListView(request):
    content = {}
    supervisor = User.objects.filter(email=request.user)
    if supervisor.exists():
        workers = Worker.objects.filter(supervisor=supervisor[0])
        if workers.exists():
            content['workers'] = workers
            if workers.count() < supervisor[0].under_worker:
                content['add_worker'] = 'yes'
    return render(request, 'stock/user/index.html', content)


def CreateView(request):
    form = forms.RegisterForm(request.POST or None)
    content = {}
    if request.POST:
        if form.is_valid():
            form.save()
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            request.session['supervisor'] = user.email
            return redirect('stock:index_user')
    content['form'] = form
    return render(request, 'stock/user/create.html', content)


def LoginView(request):
    form = forms.LoginForm(request.POST or None)
    content = {
        'form': form
    }
    if request.POST:
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                request.session['supervisor'] = user.email
                return redirect('stock:index_user')
    return render(request, 'stock/user/login.html', content)


def LogoutView(request):
    logout(request)
    return redirect('stock:index')


def WorkerView(request):
    user = User.objects.filter(email=request.user.email)
    if not user.exists():
        return redirect('stock:login_user')
    worker = Worker.objects.filter(supervisor=user[0])
    if worker.exists():
        if worker.count() >= user[0].under_worker:
            return redirect('stock:index_user')

    form = forms.WorkerForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            worker = Worker(
                supervisor=user[0],
                username=form.cleaned_data['username'],
                password=hashlib.sha512(
                    form.cleaned_data['password'].encode('utf-8')).hexdigest()
            )
            worker.save()
            return redirect('stock:index_user')

    content = {'form': form}

    return render(request, 'stock/user/worker.html', content)


def WorkerLoginView(request):
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
    return render(request, 'stock/user/workerlogin.html', content)


def EditWorkerView(request, pk):
    content = {}
    if not is_supervisor(request):
        return redirect('stock:login_user')
    if not is_worker(get_supervisor(request), pk):
        return redirect('stock:index_user')
    worker = get_worker(get_supervisor(request), pk)
    form = forms.EditWorkerForm(request.POST or None, instance=worker)
    if request.POST:
        if form.is_valid():
            if 'DELETE' in request.POST:
                user = authenticate(email=request.user, password=request.POST['verifypwd'])
                if user:
                    worker.delete()
                    return redirect('stock:index_user')
                else:
                    content['message'] = 'cannot delete password wrong'
            else:
                worker.access_level = form.cleaned_data['access_level']
                worker.save()
                return redirect('stock:index_user')
    content['form'] = form
    content['name'] = worker.username
    return render(request, 'stock/user/edit_worker.html', content)


def is_supervisor(request):
    user = User.objects.filter(email=request.user)
    if user.exists():
        return True
    return False


def get_supervisor(request):
    user = User.objects.get(email=request.user)
    return user


def is_worker(supervisor,pk):
    worker = Worker.objects.filter(supervisor=supervisor,id=pk)
    if worker.exists():
        return True
    return False


def get_worker(supervisor,pk):
    worker = Worker.objects.get(supervisor=supervisor,id=pk)
    return worker

