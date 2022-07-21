from django.db import models


class User(models.Model):
    img = models.ImageField(upload_to='profile/%Y/%m/%d', default='profile/default.jpg')
    name = models.TextField()
    email = models.EmailField()
    password = models.TextField()
    accessToken = models.TextField()
    max_day = models.DateField()
    refreshToken = models.TextField(primary_key=True)
    # point = models.IntegerField(default=0)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    imgurl = models.ImageField(upload_to='Product/', blank=True)
    types = models.TextField()
    prise = models.IntegerField()

    # top_size = models.ForeignKey('top_Size', on_delete=models.DO_NOTHING, null=True, blank=True)
    # pants_size = models.ForeignKey('pants_Size', on_delete=models.DO_NOTHING, null=True, blank=True)
    # shoes_size = models.ForeignKey('shoes_Size', on_delete=models.DO_NOTHING, null=True, blank=True)
    # colors = models.ForeignKey('Color', on_delete=models.DO_NOTHING)
    # sale = models.IntegerField(default=0)
    # shipping_money = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Check_Product(models.Model):
    product_by = models.ForeignKey('Product', on_delete=models.CASCADE)
    user_by = models.ForeignKey('User', on_delete=models.CASCADE)


class Basket(models.Model):
    id = models.AutoField(primary_key=True)
    product_by = models.ForeignKey('Product', on_delete=models.CASCADE)
    user_by = models.ForeignKey('User', on_delete=models.CASCADE)
    size = models.TextField()
    colors = models.TextField()
    # num = models.IntegerField(default=1)
    Basket_buy_by = models.ForeignKey('Basket_buy', on_delete=models.CASCADE, null=True, blank=True)


class buyReady(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    size = models.TextField()
    colors = models.TextField()


class buy(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    size = models.TextField()
    colors = models.TextField()
    # num = models.IntegerField(default=1)
    # point = models.IntegerField(default=0)
    # coupon = models.ForeignKey('Coupon', on_delete=models.DO_NOTHING)
    shipping_name = models.TextField()
    shipping_number = models.TextField()
    shipping_address = models.TextField()
    shipping_text = models.TextField()
    prise = models.IntegerField()
    prise_by = models.TextField()
    bate = models.DateTimeField(auto_now_add=True)


class Basket_buy(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    # point = models.IntegerField(default=0)
    # coupon = models.ForeignKey('Coupon', on_delete=models.DO_NOTHING)
    shipping_name = models.TextField()
    shipping_number = models.TextField()
    shipping_address = models.TextField()
    shipping_text = models.TextField()
    prise = models.IntegerField()
    prise_by = models.TextField()
    bate = models.DateTimeField(auto_now_add=True)


# 보류

class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    user_by = models.ForeignKey('User', on_delete=models.CASCADE)
    sale = models.IntegerField()
    use = models.BooleanField()


class shoes_Size(models.Model):
    size_210 = models.BooleanField()
    size_220 = models.BooleanField()
    size_230 = models.BooleanField()
    size_240 = models.BooleanField()
    size_250 = models.BooleanField()
    size_260 = models.BooleanField()
    size_270 = models.BooleanField()
    size_280 = models.BooleanField()
    size_290 = models.BooleanField()
    size_300 = models.BooleanField()
    size_310 = models.BooleanField()
    size_320 = models.BooleanField()


class top_Size(models.Model):
    XS = models.BooleanField()
    S = models.BooleanField()
    M = models.BooleanField()
    L = models.BooleanField()
    XL = models.BooleanField()
    XXL = models.BooleanField()
    XXXL = models.BooleanField()


class pants_Size(models.Model):
    size_25 = models.BooleanField()
    size_26 = models.BooleanField()
    size_27 = models.BooleanField()
    size_28 = models.BooleanField()
    size_29 = models.BooleanField()
    size_30 = models.BooleanField()
    size_32 = models.BooleanField()
    size_34 = models.BooleanField()
    size_36 = models.BooleanField()
    size_38 = models.BooleanField()


class Color(models.Model):
    red = models.BooleanField()
    yellow = models.BooleanField()
    Beige = models.BooleanField()
    green = models.BooleanField()
    blue = models.BooleanField()
    Navy = models.BooleanField()
    grey = models.BooleanField()
    white = models.BooleanField()
    black = models.BooleanField()
