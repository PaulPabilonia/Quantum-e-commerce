from os import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist", views.createlist, name="createlist"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("all_list", views.all_list, name="all_list"),
    path("submit_listings", views.submit_listings, name="submit_listings"),
    path('category',views.category, name = "category"),
    path('category_all_list',views.category_all_list,name ="category_all_list"),
    path("display_list/<int:listing_id>",views.display_list, name = "display_list"),
    path("add_add_to_cart/<int:listing_id>", views.add_add_to_cart, name = "add_add_to_cart"),
    path("remove_add_to_cart/<int:listing_id>",views.remove_add_to_cart,name="remove_add_to_cart"),
    path("closed_auction/<int:listing_id>",views.closed_auction,name="closed_auction"),
    path("add_comment/<int:listing_id>",views.add_comment,name="add_comment")
]
