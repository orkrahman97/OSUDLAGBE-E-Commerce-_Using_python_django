from django.urls import path

from . import views 

app_name = 'store_app'



urlpatterns = [
        path('',views.home.as_view(),name='home'),
        path('product/<pk>/', views.Product_detail.as_view(), name='product_detail'),
]