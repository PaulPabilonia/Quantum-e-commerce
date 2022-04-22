from os import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path("add_comment/<int:listing_id>",views.add_comment,name="add_comment"),
    path("quanta_home",views.quanta_home,name="quanta_home"),
    path("view_profile",views.view_profile,name="view_profile"),
    path("user_products",views.user_products,name="user_products"),
    path("contact",views.contact,name="contact"),
    path("my_favorites", views.my_favorites, name="my_favorites"),
    path("add_to_favorites/<int:listing_id>", views.add_to_favorites, name = "add_to_favorites"),
    path("removed_to_favorites/<int:listing_id>",views.removed_to_favorites,name="removed_to_favorites"),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="quanta/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="quanta/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="quanta/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="quanta/password_reset_done.html"), 
        name="password_reset_complete"),
]
