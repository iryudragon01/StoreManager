from stock.models import User, Worker


def is_url_exists(url):
    query = User.objects.filter(url=url)
    if query.exists():
        return True
    else:
        return False


def get_user(url):
    return User.objects.get(url=url)


def is_worker_exists(url, username=False, pk=False):
    if not is_url_exists(url):
        return False
    query = Worker.objects.all()
    if pk:
        query = Worker.objects.filter(
            supervisor=get_user(url),
            username=username
        )
    if username:
        query = Worker.objects.filter(
            supervisor=get_user(url),
            id=pk
        )
    if query.exists():
        return True
    else:
        return False


def get_worker(url, username=False, pk=False):
    if pk:
        return Worker.objects.get(
            supervisor=get_user(url),
            username=username
        )
    if username:
        return Worker.objects.get(
            supervisor=get_user(url),
            pk=pk
        )


def is_session_match(track, username, url):
    worker = get_worker(url=url, username=username)
    if track == worker.track:
        return True
    else:
        return False
