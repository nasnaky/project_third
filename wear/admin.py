from django.contrib import admin
from .models import User,buy,Basket_buy,Basket,Product,Check_Product

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Check_Product)
admin.site.register(buy)
admin.site.register(Basket)
admin.site.register(Basket_buy)




