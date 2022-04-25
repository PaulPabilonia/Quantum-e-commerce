from django.contrib import admin
from .models import User,UserProfile,Comments, ShoppingList
# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(ShoppingList)
admin.site.register(Comments)