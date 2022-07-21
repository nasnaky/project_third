from rest_framework import serializers
from .models import User, buy, Basket_buy, Basket, Product, Check_Product, buyReady


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id', 'img', 'name', 'accessToken', 'max_day', 'refreshToken']
        depth = 1


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['img', 'name', 'email', 'password']
        depth = 1


class ProductDetailSerializer(serializers.ModelSerializer):
    # top_size = top_SizeSerializer
    # pants_size = pants_SizeSerializer
    # shoes_size = shoes_SizeSerializer
    # colors = ColorSerializer

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'imgurl', 'prise']
        depth = 1


class Check_ProductUPSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField()

    class Meta:
        model = Check_Product
        fields = ['product']
        depth = 1


class Check_ProductListSeral(serializers.ModelSerializer):
    product_by = ProductListSerializer()

    class Meta:
        model = Check_Product
        fields = ['product_by']
        depth = 1


class BaskerUPSerializer(serializers.ModelSerializer):
    product_by = serializers.IntegerField()

    class Meta:
        model = Basket
        fields = ['product_by', 'size', 'colors']


class BaskerListSerializer(serializers.ModelSerializer):
    product_by = ProductListSerializer()

    class Meta:
        model = Basket
        fields = ['id', 'product_by', 'size', 'colors']


class buyReadySerializer(serializers.ModelSerializer):
    product = serializers.IntegerField()

    class Meta:
        model = buyReady
        fields = ['product', 'size', 'colors']


class buySetSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = buyReady
        fields = ['product', 'size', 'colors']


class buyUPSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField()

    class Meta:
        model = buy
        fields = ['id', 'product', 'size', 'colors', 'shipping_name', 'shipping_number', 'shipping_address',
                  'shipping_text',
                  'prise', 'prise_by', 'user']
        read_only_fields = ['id', 'user']


class Basket_buy_up_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Basket_buy
        fields = ['id', 'shipping_name', 'shipping_number', 'shipping_address', 'shipping_text', 'prise', 'prise_by',
                  'bate']
        read_only_fields = ['id', 'user']

# class CouponSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Coupon
#        fields = ['sale', 'use']
#        depth = 1
#
# class ColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Color
#         fields = '__all__'
#         depth = 1
#
#
# class top_SizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = top_Size
#         fields = '__all__'
#         depth = 1
#
#
# class shoes_SizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = shoes_Size
#         fields = '__all__'
#         depth = 1
#
#
# class pants_SizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = pants_Size
#         fields = '__all__'
#         depth = 1
