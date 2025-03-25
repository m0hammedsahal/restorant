from django.urls import path
from web import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path('singlerest/<int:id>/', views.singlerest, name="singlerest"),
    path('restorant/<int:id>/', views.restorant, name="restorant"),
    path('add_cart/<int:id>/', views.add_cart, name="add_cart"),
    path('confirm_delete_cart/<int:id>/', views.confirm_delete_cart, name='confirm_delete_cart'),
    path('add_cart_confirm/<int:id>/', views.add_cart_confirm, name='add_cart_confirm'),
    path('cart_plus/<int:id>/', views.cart_plus, name="cart_plus"),
    path('cart_minus/<int:id>/', views.cart_minus, name="cart_minus"),
    path('cart/', views.cart, name="cart"),
    path('offers/', views.offers, name="offers"),
    path('apply_cupon/', views.apply_cupon, name="apply_cupon"),
    path('calculate_cart_details/', views.calculate_cart_details, name="calculate_cart_details"),
    path('add_address/', views.add_address, name="add_address"),
    path('address/', views.address, name="address"),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('set_address/<int:id>/', views.set_address, name='set_address'),
    path('checkout/', views.checkout, name="checkout"),
    path('order_confirmation/<str:order_id>/', views.order_confirmation, name='order_confirmation'),

    path('account/', views.account, name="account"),
    path('orders/', views.orders, name="orders"),
    path('order_tracking/<int:id>/', views.order_tracking, name='order_tracking'),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),

    
    path("ajaxlogin/", views.ajaxlogin, name="ajaxlogin"),
    path("validate_email/", views.validate_email, name="validate_email"),
    
    path("ajaxlogin2/", views.ajaxlogin2, name="ajaxlogin2"),
    
    path('ajax/', views.ajax, name="ajax"),
    path('updatecart/', views.updatecart, name="updatecart"),
]