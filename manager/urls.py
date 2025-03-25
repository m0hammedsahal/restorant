from django.urls import path
from manager import views

app_name = "manager"


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("unauthorized_access/", views.unauthorized_access, name="unauthorized_access"),
    # path("orders", views.orders, name="orders"),
    path("orders/list/", views.orders_list, name="orders_list"),
    path("orders/edit/<int:id>/", views.orders_edit, name="orders_edit"),
    path("orders/delete/<int:id>/", views.orders_delete, name="orders_delete"),

    path("orders/track/list/", views.orders_track_list, name="orders_track_list"),
    path("order/Track/<int:id>/", views.order_track, name="order_track"),
    path("order/Cancel/<int:id>/", views.cancel_order, name="cancel_order"),

    # path("store-category", views.store_category, name="store_category"),
    path("store-category/list/", views.store_category_list, name="store_category_list"),
    path("store-category/add/", views.store_category_add, name="store_category_add"),
    path("store-category/edit/<int:id>/", views.store_category_edit, name="store_category_edit"),
    path("store-category/delete/<int:id>/", views.store_category_delete, name="store_category_delete"),

    
    # path("slide", views.slide, name="slide"),
    path("slide/list/", views.slide_list, name="slide_list"),
    path("slide/add/", views.slide_add, name="slide_add"),
    path("slide/edit/<int:id>/", views.slide_edit, name="slide_edit"),
    path("slide/delete/<int:id>/", views.slide_delete, name="slide_delete"),
    
    # path("restorant", views.slide, name="restorant"),
    path("restorant/list/", views.restorant_list, name="restorant_list"),
    path("restorant/add/", views.restorant_add, name="restorant_add"),
    path("restorant/edit/<int:id>/", views.restorant_edit, name="restorant_edit"),
    path("restorant/delete/<int:id>/", views.restorant_delete, name="restorant_delete"),
    
    # path("food-category", views.slide, name="food_category"),
    path("food-category/list/", views.food_category_list, name="food_category_list"),
    path("food-category/add/", views.food_category_add, name="food_category_add"),
    path("food-category/edit/<int:id>/", views.food_category_edit, name="food_category_edit"),
    path("food-category/delete/<int:id>/", views.food_category_delete, name="food_category_delete"),
    

    # path("food-item", views.slide, name="food_item"),
    path("food-item/list/", views.food_item_list, name="food_item_list"),
    path("food-item/add/<int:id>/", views.food_item_add, name="food_item_add"),
    path("food-item/foodcategoory/add/<int:id>/", views.food_item_add_f_cate, name="food_item_add_f_cate"),
    path("food-item/edit/<int:id>/", views.food_item_edit, name="food_item_edit"),
    path("food-item/delete/<int:id>/", views.food_item_delete, name="food_item_delete"),


    # path("offers", views.slide, name="offers"),
    path("offers/list/", views.offers_list, name="offers_list"),
    path("offers/add/", views.offers_add, name="offers_add"),
    path("offers/edit/<int:id>/", views.offers_edit, name="offers_edit"),
    path("offers/delete/<int:id>/", views.offers_delete, name="offers_delete"),
    
    # path("users", views.users, name="users"),
    path("users/list/", views.users_list, name="users_list"),


]