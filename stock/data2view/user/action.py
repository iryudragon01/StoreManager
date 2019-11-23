from stock.models import User, Worker
import string, random, hashlib
from . import queries


def UserContent(request):
    content = {}
    if 'supervisor' in request.session:
        content['supervisor'] = request.session['supervisor']
    if 'worker' in request.session:
        content['worker'] = request.session['worker']
    return content


def update_track(length=55):
    letters = string.ascii_lowercase
    track = ''.join(random.choice(letters) for i in range(length))
    return track


def hash_pwd(password):
    hash_pass = hashlib.sha512(password.encode('utf-8')).hexdigest()
    return hash_pass


def create_worker(request, url, username, password,access_level=99):
    user = queries.get_user(url)
    worker = Worker(supervisor=user,
                    username=username,
                    password=hash_pwd(password),
                    access_level=access_level)
    if username == 'admin':
        worker.access_level = 1
    worker.save()
    return


def set_worker(request, url, username):
    track = update_track()
    worker = queries.get_worker(url=url, username=username)
    worker.track = track
    worker.save()
    request.session['worker'] = worker.username
    request.session['track'] = track
    request.session['url'] = url
    request.session['access_level'] = worker.access_level
    return


def clear_worker(request):
    try:
        del request.session['supervisor']
        del request.session['worker']
        del request.session['track']
        del request.session['url']
        del request.session['access_level']
    except KeyError:
        pass
    return
