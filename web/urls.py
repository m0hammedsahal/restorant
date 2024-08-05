from django.urls import path
from web import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path('singlerest/<int:id>/', views.singlerest, name="singlerest"),
    path('restorant/<int:id>/', views.restorant, name="restorant"),
    path('add_cart/<int:id>/', views.add_cart, name="add_cart"),
    path('cart_plus/<int:id>/', views.cart_plus, name="cart_plus"),
    path('cart_minus/<int:id>/', views.cart_minus, name="cart_minus"),
    path('cart_total/<int:id>/', views.cart_total, name="cart_total"),
    path('cart/', views.cart, name="cart"),
    path('offers/', views.offers, name="offers"),
    path('account/', views.account, name="account"),
    path('checkout/', views.checkout, name="checkout"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),

]