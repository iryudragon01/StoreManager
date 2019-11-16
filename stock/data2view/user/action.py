from stock.models import User


def create(form):
    print(form.POST['username'])
