from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'add-to-cart/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'buy-now/<int:product_id>/',
        views.buy_now,
        name='buy_now'
    ),

    path(
        'update/<int:item_id>/<str:action>/',
        views.update_quantity,
        name='update_quantity'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'checkout-success/',
        views.checkout_success,
        name='checkout_success'
    ),

    path(
        'orders/',
        views.order_history,
        name='order_history'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),
]