from django.urls import path
from . import views
from .data2view.item import views as itemview
from .data2view.user import views as userview
from stock.data2view.index import views as indexview
from stock.data2view.store import views as storeview


app_name = 'stock'

urlpatterns = [
    path('',indexview.IndexView, name='index'),


    # item
    path('create_item/',itemview.CreateView,name='create_item'),

    # store
    path('store/<str:url>',storeview.IndexView, name='index_store'),
    path('store/<str:url>/list/worker',storeview.ListView, name='list_worker'),
    path('store/<str:url>/create/worker/',storeview.WorkerCreateView, name='create_worker'),
    path('stork/<str:url>/edit/worker/<int:pk>',storeview.EditWorkerView, name='edit_worker'),
    path('store/<str:url>/login/worker/', storeview.WorkerLoginView, name='login_worker'),
    path('store/<str:url>/display/sum/',storeview.SumView, name='display_sum'),

    # user
    path('create_user/',userview.CreateView,name='create_user'),
    path('login_user/',userview.LoginView,name='login_user'),
    path('logout/',userview.LogoutView,name='logout_user'),



    # AJAX
    path('ajax/',indexview.AjaxView, name='ajax'),

]