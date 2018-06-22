import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from .models import *
import django
import hashlib
# Create your views here.

#首页
def home(request):
    wheelsList = Wheel.objects.all()
    # 顶部菜单数据
    navs = Nav.objects.all()

    mustbuys = Mustbuy.objects.all()

    shop = Shop.objects.all()
    shop0 = shop.first()
    shop1_2 = shop[1:3]
    shop3_6 = shop[3:7]
    shop7_10 = shop[7:11]

    mainshows = Mainshow.objects.all()

    data = {
        'title':'首页',
        'wheelsList':wheelsList,
        'navs':navs,
        'mustbuys':mustbuys,
        'shop0':shop0,
        'shop1_2': shop1_2,
        'shop3_6':shop3_6,
        'shop7_10':shop7_10,
        'mainshows':mainshows,
    }
    return render(request, 'home/home.html',data)

#闪购
def market(request):
    return redirect(reverse('app:market_with_params', args=('104749','0','0')))


def market_with_params(request, typeid, cid, sort_id):
    foodtypes = Foodtypes.objects.all()
    # 商品数据
    goods_list = Goods.objects.filter(categoryid=typeid)

    if cid != "0":
        goods_list = goods_list.filter(childcid=cid)

    # 获取当前主分类下的所有子分类
    all_child_type = []
    current_types =  foodtypes.filter(typeid = typeid)
    if current_types.exists():
        current_types = current_types.first()
        childtypenames = current_types.childtypenames
        child_type_list = childtypenames.split('#')

        for s in child_type_list:
            l = s.split(':')
            all_child_type.append(l)


    # 排序规则：
    if sort_id =='0':
       pass
    elif sort_id == '1':
        goods_list = goods_list.order_by('-productnum')
    elif sort_id =='2':
        goods_list = goods_list.order_by('-price')
    elif sort_id =='3':
        goods_list = goods_list.order_by('price')


    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'typeid':typeid,
        'all_child_type':all_child_type,
        'cid':cid,
    }
    return render(request, 'market/market.html', data)



def taobao(request, name):
    url= 'https://s.taobao.com/search?q='+ name
    return redirect(url)


#我的
def mine(request):

    data = {
        'title': '我的',
        'username':'',
        'icon': '',
    }

    # 从session中获取登录的id
    user_id = request.session.get('user_id','')

    #判断是否为登录状态
    if user_id:
        users = UserModel.objects.filter(id = user_id)
        if users.exists():
            user = users.first()
            data['username'] = user.username
            if user.icon:
                data['icon'] = 'uploads/'+ user.icon.url

    return render(request, 'mine/mine.html',data)

# 我的-注册

def register(request):
    data = {
        'status':'200',
        'msg': 'ok',
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon', None)

        if len(username)<8:
            data['status'] = '0'
            data['msg'] = '失败'
            return render(request, 'user/register.html')


        try:
            user = UserModel()
            user.username = username
            user.password = password
            user.email = email
            user.icon = icon
            user.save()

            #注册成功后，进入'我的页面'
            request.session['user_id'] = user.id
            return redirect(reverse('app:mine'))

        except Exception as e:
            # print(e)
            data['status'] = '-1'
            data['msg'] = '失败'
            return render(request, 'user/register.html')
    else:
        return render(request, 'user/register.html')


#删除session 注销
def logout(request):
    request.session.flush()
    return redirect(reverse('app:mine'))

#检测用户名是否已经存在
def checkname(request):
    data = {
        'status':1,
        'msg':'OK'
    }
    if request.method == 'GET':
        username = request.GET.get('username')
        users = UserModel.objects.filter(username=username)

        if users.exists():
            data['status'] = 0
            data['msg'] = '用户名已经存在'

    else:
        data['status'] = -1
        data['msg'] = '请求方式错误'

    return JsonResponse(data)

# 我的登录
def login(request):

    data = {
        'status':1,
        'msg':'ok'
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 直接匹配用户名和密码在数据库中是否存在
        '''
        users = UserModel.objects.filter(username = username, password=password)
        if users.exists():
            request.session['user_id'] = users.first().id
            return redirect(reverse('app:mine'))
            
        '''
        #先验证是否存在用户名再匹配密码
        users = UserModel.objects.filter(username=username)
        if users.exists():
            user = users.first()
            if user.password == password:
                request.session['user_id'] = users.first().id
                return redirect(reverse('app:mine'))
            else:
                data['status'] = 0
                data['msg'] = '密码输入不正确'
        else:
            data['status'] = -1
            data['msg'] = '用户不存在'

        return render(request, 'user/login.html', data)

    else:
        return render(request, 'user/login.html', data)

#购物车
def cart(request):

    # 先检查是否登录了
    user_id = request.session.get('user_id','')
    if not user_id:
        return redirect(reverse('app:login'))

    else:

    # 获取购物车表的所有商品数据
        carts = CartModel.objects.filter(user_id=user_id)

        data = {
            'title': '购物车',
            'carts' : carts,
        }
        return render(request, 'cart/cart.html',data)

# 加入购物车
def add_to_cart(request):
    data = {
        'status': 1,
        'msg':'ok',
    }
    # 先判断用户是否已经登录
    user_id = request.session.get('user_id','')
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'
    else:
        if request.method == 'GET':
            goods_id = request.GET.get('goodsid')
            num = request.GET.get('num')
            # 判断商品是否已经存在
            res = CartModel.objects.filter(goods_id=goods_id, user_id=user_id)
            if res.exists():
                new_num = res.first().num + int(num)
                res.update(num=new_num)

    #         加入购物车
            else:
                cart = CartModel()
                cart.user_id = user_id
                cart.goods_id = goods_id
                cart.num = num
                cart.save()

        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


#数量增加1
def add_num(request):
    data = {
        'status':1,
        'msg':'ok',

    }

    # 1、判断用户是否登录
    #2、将当前用户对应的购物车商品数量+1

    user_id = request.session.get('user_id','')
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'

    else:
        if request.method =='GET':
           cart_id = request.GET.get('cartid')
           cart = CartModel.objects.get(pk=cart_id)
           cart.num += 1
           cart.save()
           data['num'] = cart.num
        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'

    return JsonResponse(data)

# 数量减1
def sub_num(request):
    data = {
        'status':1,
        'msg':'ok',

    }

    # 1、判断用户是否登录
    #2、将当前用户对应的购物车商品数量+1

    user_id = request.session.get('user_id','')
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'

    else:
        if request.method =='GET':
           cart_id = request.GET.get('cartid')
           cart = CartModel.objects.get(pk=cart_id)
           cart.num -= 1
           if cart.num < 1:
               cart.num = 1
           cart.save()
           data['num'] = cart.num
        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'

    return JsonResponse(data)

# 勾选
def change_select_state(request):
    data = {
        'status': 1,
        'msg': 'ok',

    }

    # 1、判断用户是否登录

    user_id = request.session.get('user_id', '')
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'

    else:
        if request.method == 'GET':
            cart_id = request.GET.get('cartid')
            cart = CartModel.objects.get(pk=cart_id)
            cart.is_select = not cart.is_select
            cart.save()
            # 将最新的勾选状态返回
            data['select'] = cart.is_select
        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'
    return JsonResponse(data)

# 删除
def cart_del_goods(request):
    data = {
        'status': 1,
        'msg': 'ok',

    }

    # 1、判断用户是否登录

    user_id = request.session.get('user_id', '')
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'

    else:
        if request.method == 'GET':
            cart_id = request.GET.get('cartid')
            cart = CartModel.objects.get(pk=cart_id)
            cart.delete()
        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 全选/全不选
def cart_change_select(request):
    data = {
        'status': 1,
        'msg': 'ok',

    }

    # 1、判断用户是否登录

    user_id = request.session.get('user_id', '')
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'
    # 已登录
    else:
        if request.method == 'GET':
            selects = request.GET.get('selects')
            select_list = selects.split('#')
            action = request.GET.get('action')
            #全不选
            if action == 'unselect':
                CartModel.objects.filter(id__in=select_list).update(is_select=False)

            # 全选
            else:
                CartModel.objects.filter(id__in=select_list).update(is_select=True)

        else:
            data['status'] = -1
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


# 生成订单
def generate_order(request):
    data = {
        'status':1,
        'msg':'ok',
    }

    user_id = request.session.get('user_id','')
    # 未登录

    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'

    else:
        if request.method == 'GET':
            selects = request.GET.get('selects')
            select_list = selects.split('#')
            print(select_list)



            # 生成订单
            order = OrderModel()
            order.user_id = user_id
            order.order_id = str(uuid.uuid4())
            order.save()

            # 生成订单商品数据
            total = 0
            for cartid in select_list:
                cart = CartModel.objects.get(id=cartid)

                order_goods = OrderGoodsModel()

                order_goods.order_id = order.id
                # print(order.id,cart.goods.id, cart.num,cart.goods.price )
                order_goods.goods_id = cart.goods.id
                order_goods.num = cart.num
                order_goods.price = cart.goods.price
                order_goods.save()

                total += int(order_goods.num)*float(order_goods.price)
                order.order_price = total
                order.save()
                data['orderid'] = order.id

            # 删除购物车中勾选商品
                cart.delete()


        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'

    return JsonResponse(data)


#获得订单信息
def order_info(request , order_id):
    order = OrderModel.objects.get(id=order_id)

    data = {
        'order':order,
    }
    return  render(request, 'order/orderinfo.html', data)

# 改变订单状态
def change_order_status(request):
    data = {
        'status':1,
        'msg':'ok',
    }

    user_id = request.session.get('user_id', '')
    if not user_id:
        data['status'] = -1
        data['msg'] = '请先登录'
    else:
        if request.method == "GET":
            orderid = request.GET.get('orderid')
            status = request.GET.get('status')
            order = OrderModel.objects.get(id = orderid)
            order.order_status = 1
            order.save()

        else:
            data['status'] = 0
            data['msg'] = '请求方式错误'

        return JsonResponse(data)


# 待付款
def order_wait_pay(request):

    orders = OrderModel.objects.filter(order_status='0')

    data = {
        'orders':orders,
    }
    return render(request,'order/orderwaitpay.html',data)



# 待收货
def orderpayd(request):

    orders = OrderModel.objects.filter(order_status='1')

    data = {
        'orders':orders,
    }
    return render(request,'order/orderpayd.html',data)
