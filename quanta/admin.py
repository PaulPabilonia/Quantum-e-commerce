from django.contrib import admin
from .models import User,Comments, ShoppingList, CheckoutOrder
# Register your models here.
admin.site.register(User)
admin.site.register(ShoppingList)
admin.site.register(Comments)
admin.site.register(CheckoutOrder)