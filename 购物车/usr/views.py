import random

import time
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from usr.models import MainWheel, MainShow, MainNav, MainMustBuy, MainShop, UserModel, UserTicketModel, FootType, \
    OrderModel, Goods, CartModel, OrderGoodsModel


# Create your views here.


def home(request):
    wheel = MainWheel.objects.all()
    nav = MainNav.objects.all()
    mustbuy = MainMustBuy.objects.all()
    shops = MainShop.objects.all()

    shows = MainShow.objects.all()

    data = {
        'wheel': wheel,
        'nav': nav,
        'mustbuy': mustbuy,
        'shops': shops,
        'shows': shows,
    }

    return render(request, 'home/home.html', data)


def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        password = make_password(password)
        email = request.POST.get('email')
        # if request.POST.get('sex') == '男':
        #     sex = 1
        # else:
        #     sex = 0
        icon = request.FILES.get('icon')

        UserModel.objects.create(
            username=name,
            password=password,
            email=email,
            icon=icon,
        )
        return HttpResponseRedirect('/usr/login/')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        if UserModel.objects.filter(username=name).exists():
            users = UserModel.objects.get(username=name)
            if check_password(password, users.password):
                s = 'qwertyuiiiopasdfghjklzxcvbnm1234567890'
                ticket = ''
                for _ in range(15):
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket = 'TK' + ticket + str(now_time)

                # resopnse.set_cookie('ticket',ticket)
                # user.ticket = ticket
                # user.save()

                response = HttpResponseRedirect(reverse('axf:mine'))
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires=out_time)
                UserTicketModel.objects.create(
                    u_user_id=users.id,
                    ticket=ticket,
                    ticket_out_time=out_time
                )
                return response

            else:
                return render(request, 'user/user_login.html', {'password': '用户密码错误'})
    else:
        return render(request, 'user/user_login.html', {'name': '用户名不存在'})


def logout(request):
    if request.method == 'GET':
        # 删除cookie
        response = HttpResponseRedirect('/usr/home')
        response.delete_cookie('ticket')
        ticket = request.COOKIES.get('ticket')
        UserTicketModel.objects.filter(ticket=ticket).delete()
        return response


def market(request):
    return HttpResponseRedirect(reverse('axf:smarketpragram', args=('104749', '0', '0')))


def marketpragram(request, typeid, cid, sort_id):
    if request.method == 'GET':
        foottypes = FootType.objects.all()
        foottype_childnames = FootType.objects.filter(typeid=typeid).first()
        childtypenames_list = foottype_childnames.childtypename.split('#')
        child_types_list = []
        for childtypename in childtypenames_list:
            child_types_list.append(childtypename.split(':'))
        if cid == '0':
            goods_types = Goods.objects.filter(categoryid=typeid)
        else:
            goods_types = Goods.objects.filter(categoryid=typeid, childcid=cid)

        if sort_id == '0':
            pass
        elif sort_id == '1':
            goods_types = goods_types.order_by('specifics')
        elif sort_id == '2':
            goods_types = goods_types.order_by('-price')
        elif sort_id == '3':
            goods_types = goods_types.order_by('price')

        data = {
            'foottypes': foottypes,
            'goods_types': goods_types,
            'typeid': typeid,
            'cid': cid,
            'sort_id': sort_id,
            'child_types_list': child_types_list
        }
    return render(request, 'market/market.html', data)


def mine(request):
    if request.method == 'GET':
        user = request.user
        data = {}
        if user.id and user:
            orders = user.ordermodel_set.all()
            wait_pay, payed = 0, 0

            for order in orders:
                if order.o_status == 0:
                    wait_pay += 1
                elif order.o_status == 1:
                    payed += 1
            data['wait_pay'] = wait_pay
            data['payed'] = payed

        return render(request, 'mine/mine.html', data)


def addgoods(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': '200',
        }
    user = request.user
    goods_id = request.POST.get('goods_id')
    if user and user.id:
        user_cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()

        if user_cart:
            user_cart.c_num += 1
            user_cart.save()
            data['c_num'] = user_cart.c_num
        else:
            CartModel.objects.create(user=user,
                                     goods_id=goods_id,
                                     c_num=1)
            data['c_num'] = 1
        total = sum()
        data['total'] = total

    return JsonResponse(data)


def subgoods(request):
    if request.method == 'POST':

        data = {
            'msg': '请求成功',
            'code': '200',
        }
        user = request.user
        goods_id = request.POST.get('goods_id')
        if user and user.id:
            user_cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()

            if user_cart:
                if user_cart.c_num == 1:
                    user_cart.delete()
                    data['c_num'] = 0

                else:
                    user_cart.c_num -= 1

                    user_cart.save()
                    data['c_num'] = user_cart.c_num
                total = sum()
                data['total'] = total

        return JsonResponse(data)


def cart(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            carts = CartModel.objects.filter(user=user)
            total = sum()
            all_select = is_allsel()

            return render(request, 'cart/cart.html', {'carts': carts, 'total': total, 'all_select':all_select})
        else:
            return HttpResponseRedirect(reverse('axf:login'))


# 判断order的每个商品是否is_select，即可判断是否为全选
def is_allsel():
    all_sel = True
    carts = CartModel.objects.all()
    for cart in carts:
        if not cart.is_select:
            all_sel = False
        return all_sel


def select_goods(request):
    if request.method == 'POST':
        user = request.user
        data = {
            'msg': '请求成功',
            'code': '200',
        }
        cart_id = request.POST.get('cart_id')

        if user and user.id:

            cart = CartModel.objects.filter(pk=cart_id).first()
            if cart.is_select:
                cart.is_select = False
            else:
                cart.is_select = True

            cart.save()
            total = sum()
            allsel = is_allsel()
            data['total'] = total
            data['is_select'] = cart.is_select
            data['allsel'] = allsel

        return JsonResponse(data)


def ordergoods(request):
    if request.method == 'GET':
        # 判断is_select为真的商品信息
        user = request.user
        if user and user.id:
            cart_goods = CartModel.objects.filter(is_select=True)
            order = OrderModel.objects.create(user=user, o_status=0)

            for car in cart_goods:
                OrderGoodsModel.objects.create(order=order, goods=car.goods, goods_num=car.c_num)
                car.delete()

            return HttpResponseRedirect(reverse('axf:user_orderinfo', args=(str(order.id),)))


# 支付页面
def user_orderinfo(request, order_id):
    if request.method == 'GET':
        order_goods = OrderModel.objects.filter(pk=order_id).first()
        # order_goods = order.GoodsModel_set.all()

        data = {
            'order_goods': order_goods,
            'order_id': order_id
        }
        return render(request, 'order/order_info.html', data)


def change_order_status(request, order_id):
    if request.method == 'GET':
        OrderModel.objects.filter(pk=order_id).update(o_status=1)
        return HttpResponseRedirect(reverse('axf:mine'))


# 待支付
def user_wait_pay(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user, o_status=0)
            return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


# 待收货
def user_pay(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user, o_status=1)
            return render(request, 'order/order_list_payed.html', {'orders': orders})

# 计算商品总价
def sum():
    total = 0
    cart_goods = CartModel.objects.filter(is_select=True)
    for cart_good in cart_goods:
        num = cart_good.c_num
        price = cart_good.goods.price
        total += num * price
        total = float('%.2f' % total)

    return total


# 全选
def allSelectChange(request):
    if request.method == 'POST':
        user = request.user
        data = {
            'msg': '请求成功',
            'code': '200'
        }
        all_select = request.POST.get('all_select')
        if user and user.id:
            if all_select == '1':
                all_select = 0
            else:
                all_select = '1'
            carts = CartModel.objects.all()
            carts_id = []
            if all_select == '1':
                for c in carts:
                    c.is_select = True
                    carts_id.append(c.id)
                    c.save()
            else:
                for c in carts:
                    c.is_select = False
                    carts_id.append(c.id)
                    c.save()

            total = sum()
            data['allselt'] = all_select
            data['carts_id'] = carts_id
            data['total'] = total

        return JsonResponse(data)
