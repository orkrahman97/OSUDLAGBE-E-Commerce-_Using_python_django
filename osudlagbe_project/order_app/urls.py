from django.urls import path
from . import views
app_name = "order_app"

urlpatterns = [
    path('add_to_cart/<pk>/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.cart_view,name='cart'),
    path('increase/<pk>/',views.increase_cart,name='increase'),
    path('decrease/<pk>/',views.decrease_cart,name='decrease'),
    path('remove/<pk>/',views.remove_from_cart,name='remove'),
]