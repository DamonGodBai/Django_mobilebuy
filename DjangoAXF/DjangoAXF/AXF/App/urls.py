from django.conf.urls import url

from App.views import *

urlpatterns =[
    url(r'^home/$', home, name='home'),
    url(r'^market/$', market, name='market'),
    url(r'^cart/$', cart, name='cart'),
    url(r'^mine/$', mine, name='mine'),

    url(r'^market/(?P<typeid>\d+)/(?P<cid>\d+)/(?P<sort_id>\d+)$', market_with_params, name= 'market_with_params'),
    url(r'^taobao/(.+)$', taobao, name='taobao'),

    url(r'^register/$', register, name='register'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^checkusername/$', checkname, name='checkname'),

    url(r'^login/$', login, name='login'),


    url(r'^addnum/$', add_num, name='add_num'),
    url(r'^subnum/$', sub_num, name='sub_num'),


    url(r'^add_to_cart/$', add_to_cart, name='add_to_cart'),

    url(r'^changeselectstate/$', change_select_state, name='change_select_state'),
    url(r'^cartdelgoods/$', cart_del_goods, name='cart_del_goods'),
    url(r'^cartchangeselect/$', cart_change_select, name='cart_change_select'),

    url(r'^generateorder/$', generate_order, name='generate_order'),
    url(r'^orderinfo/(\d+)/$', order_info, name='order_info'),

    url(r'^changeorderstatus/$', change_order_status, name='change_order_status'),

    url(r'^orderwaitpay/$', order_wait_pay, name='orderwaitpay'),
    url(r'^orderpayd/$', orderpayd, name='orderpayd'),

]