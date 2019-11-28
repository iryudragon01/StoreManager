from django.urls import path
from . import views
from .data2view.store.item import views as itemview
from .data2view.store.sale import views as saleview
from .data2view.user import views as userview
from stock.data2view.index import views as indexview
from stock.data2view.store import views as storeview

app_name = 'stock'

urlpatterns = [
    path('bootstrap/', storeview.bootstrap, name='testbootstrap'),
    path('', indexview.IndexView, name='index'),
    #sale
    path('store/<str:url>/store/sale/index' , saleview.IndexView, name="index_sale"),
    path('store/<str:url>/store/sale/detail/<int:pk>' , saleview.DetailView, name="detail_sale"),
    path('store/<str:url>/store/sale/delete/<int:pk>' , saleview.DeleteView, name="delete_sale"),
    path('store/<str:url>/store/sale/list' , saleview.ListView, name="list_sale"),
    path('ajax/<str:url>/sale', saleview.AjaxSaleView,name='ajax_sale'),
    # item
    path('store/<str:url>/create/item/', itemview.CreateView, name='create_item'),
    path('store/<str:url>/list/item/', itemview.ListView, name='list_item'),
    path('store/<str:url>/edit/item/<int:pk>/', itemview.EditView, name='edit_item'),

    # store
    path('search/', storeview.StoreSearchView, name='search_store'),
    path('store/<str:url>', storeview.IndexView, name='index_store'),

    # worker
    path('store/<str:url>/list/worker', storeview.ListView, name='list_worker'),
    path('store/<str:url>/create/worker/', storeview.WorkerCreateView, name='create_worker'),
    path('stork/<str:url>/edit/worker/<int:pk>', storeview.EditWorkerView, name='edit_worker'),
    path('<str:url>/login/worker/', storeview.WorkerLoginView, name='login_worker'),
    path('<str:url>/logout/worker/', storeview.WorkerLogoutView, name='logout_worker'),

    path('store/<str:url>/display/sum/', storeview.SumView, name='display_sum'),

    # user
    path('create/user/', userview.CreateView, name='create_user'),
    path('login/user/', userview.LoginView, name='login_user'),
    path('logout/user/', userview.LogoutView, name='logout_user'),

    # AJAX
    path('ajax/', indexview.AjaxView, name='ajax'),

]
