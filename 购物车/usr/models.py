from django.db import models


# Create your models here.


class Main(models.Model):
    img = models.CharField(max_length=200)  # 图片
    name = models.CharField(max_length=100)  # 名称
    trackid = models.CharField(max_length=16)  # 通用ID

    class Meta:
        abstract = True


class MainWheel(Main):
    # 轮播banner
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    # 导航
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):
    # 必购
    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):
    # 商店
    class Meta:
        db_table = 'axf_shop'


class MainShow(Main):
    categoryid = models.CharField(max_length=16)
    brandname = models.CharField(max_length=100)
    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)
    longname1 = models.CharField(max_length=100)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=1)
    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)
    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_mainshow'


# 闪购
class FootType(models.Model):
    typeid = models.CharField(max_length=16)
    typename = models.CharField(max_length=100)
    childtypename = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    productid = models.CharField(max_length=16)  # 商品ID
    productimg = models.CharField(max_length=200)  # 商品图片
    productname = models.CharField(max_length=100)  # 商品名称
    productlongname = models.CharField(max_length=200)  # 商品的具体规格
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)  # 商品重量
    price = models.FloatField(default=0)  # 折后价格
    marketprice = models.FloatField(default=1)  # 原价
    categoryid = models.CharField(max_length=16)  # 分类ID
    childcid = models.CharField(max_length=16)  # 子分类ID
    childcidname = models.CharField(max_length=100)  # 子分类名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)  # 排序
    productnum = models.IntegerField(default=1)  # 销量排序

    class Meta:
        db_table = 'axf_goods'


# 用户表
class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    sex = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icons')  # 头像
    is_delete = models.BooleanField(default=False)  # 是否删除

    class Meta:
        db_table = 'axf_users'


# 购物车
class CartModel(models.Model):
    user = models.ForeignKey(UserModel)  # 关联用户
    goods = models.ForeignKey(Goods)  # 关联商品
    c_num = models.IntegerField(default=1)  # 商品个数
    is_select = models.BooleanField(default=True)  # 是否选择商品

    class Meta:
        db_table = 'axf_cart'


# 订单
class OrderModel(models.Model):
    user = models.ForeignKey(UserModel)
    o_num = models.CharField(max_length=64)
    # 0 代表已下单，但是未付款， 1 已付款未发货  2  已付款
    o_status = models.IntegerField(default=0)
    o_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'axf_order'


# 订单商品详情
class OrderGoodsModel(models.Model):
    goods = models.ForeignKey(Goods)
    order = models.ForeignKey(OrderModel)
    goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_order_goods'


class UserTicketModel(models.Model):
    u_user = models.ForeignKey(UserModel)
    ticket = models.CharField(max_length=30, null=True)
    ticket_out_time = models.DateTimeField()

    class Meta:
        db_table = 'axf_user_ticket'
