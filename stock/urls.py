from django.urls import path
from . import views
from .data2view.item import views as itemview
from .data2view.user import views as userview


app_name = 'stock'

urlpatterns = [
    path('',userview.IndexView, name='index_user'),


    # item
    path('create_item/',itemview.CreateView,name='create_item'),

    #user
    path('create_user/',userview.CreateView,name='create_user'),
    path('login_user/',userview.LoginView,name='login_user'),
    path('logout/',userview.LogoutView,name='logout_user'),
    path('create_worker/',userview.WorkerView,name='create_worker'),
    path('login_worker/',userview.WorkerLoginView, name='login_worker'),

    path('work/',userview.WorkView, name='work')
]