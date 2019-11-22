from stock.models import User
import string
import random


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
