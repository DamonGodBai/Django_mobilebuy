from django.db import models

# Create your models here.
# 首页
class Wheel(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Nav(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Mustbuy(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Shop(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Mainshow(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

    categoryid = models.CharField(max_length=100)
    brandname = models.CharField(max_length=100)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=100)
    productid1 = models.CharField(max_length=100)
    longname1 = models.CharField(max_length=100)
    price1 = models.CharField(max_length=30)
    marketprice1 = models.CharField(max_length=30)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=100)
    productid2 = models.CharField(max_length=100)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=30)
    marketprice2 = models.CharField(max_length=30)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=100)
    productid3 = models.CharField(max_length=100)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=30)
    marketprice3 = models.CharField(max_length=30)


# 闪购
# axf_foodtypes(typeid,typename,childtypenames,typesort
class Foodtypes(models.Model):
    typeid = models.CharField(max_length=20)
    typename = models.CharField(max_length=50)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

#
# insert into axf_goods(productid,productimg,productname,
#                       productlongname,isxf,pmdesc,specifics,
#                       price,marketprice,categoryid,childcid,childcidname,
#                       dealerid,storenums,productnum)

class Goods(models.Model):
    productid = models.CharField(max_length=20)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=200)
    productlongname = models.CharField(max_length=200)
    isxf = models.BooleanField(default=0)
    pmdesc = models.CharField(max_length=200)

    specifics = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=0)
    categoryid = models.CharField(max_length=20)
    childcid = models.CharField(max_length=20)
    childcidname = models.CharField(max_length=20)
    dealerid = models.CharField(max_length=20)

    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)


# 用户信息

class UserModel(models.Model):
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=40)
    email = models.EmailField()
    icon = models.ImageField()
    sex = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)


#购物车
class CartModel(models.Model):
    user = models.ForeignKey(UserModel)
    goods = models.ForeignKey(Goods)
    num = models.IntegerField()
    is_select = models.BooleanField(default=True)


# 订单
class OrderModel(models.Model):
     order_id = models.CharField(max_length=100,unique=True)
     order_create = models.DateTimeField(auto_now_add=True)
     order_price = models.FloatField(default=0)
     # 订单状态: 0表示待付款，1表示待收货， 2表示待评价 ，3表示交易完成
     order_status = models.CharField(max_length=20, default=0)
     user = models.ForeignKey(UserModel)

# 订单商品表
class OrderGoodsModel(models.Model):
    goods = models.ForeignKey(Goods)
    order = models.ForeignKey(OrderModel)
    num = models.IntegerField(default = 1)
    price = models.FloatField(default = 0)
