from django.conf.urls import url
from usr import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^market/$', views.market, name='market'),
    url(r'^smarketpragram/(\d+)/(\d+)/(\d+)/', views.marketpragram, name='smarketpragram'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^register/', views.register,name='register'),
    url(r'^login/', views.login,name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^addgoods/',views.addgoods,name='addgoods'),
    url(r'^subgoods/',views.subgoods,name='subgoods'),
    url(r'^goodsel/$',views.select_goods,name='goodsel'),
    url(r'^ordergoods/',views.ordergoods,name='ordergoods'),
    url(r'^user_orderinfo/(\d+)',views.user_orderinfo,name='user_orderinfo'),
    url(r'^change_order_status/(\d+)',views.change_order_status,name='change_order_status'),
    url(r'^user_wait_pay/$',views.user_wait_pay,name='user_wait_pay'),
    url(r'^user_pay/$',views.user_pay,name='user_pay'),
    url(r'^allselt/$',views.allSelectChange,name='allselt')




]
