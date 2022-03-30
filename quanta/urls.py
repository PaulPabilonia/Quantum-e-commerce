from os import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("login", views.login_view, name="login"),
    # path("logout", views.logout_view, name="logout"),
    # path("register", views.register, name="register"),
    # path("createlist", views.createlist, name="createlist"),
    # path("watchlist", views.watchlist, name="watchlist"),
    # path("all_list", views.all_list, name="all_list"),
    # path("submit_listings", views.submit_listings, name="submit_listings"),
    # path('category',views.category, name = "category"),
    # path('category_all_list',views.category_all_list,name ="category_all_list"),
    # path("display_list/<int:listing_id>",views.display_list, name = "display_list"),
    # path("add_watchlist/<int:listing_id>", views.add_watchlist, name = "add_watchlist"),
    # path("remove_watchlist/<int:listing_id>",views.remove_watchlist,name="remove_watchlist"),
    # path("closed_auction/<int:listing_id>",views.closed_auction,name="closed_auction"),
    # path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    # path("add_comment/<int:listing_id>",views.add_comment,name="add_comment")
]
