from django.urls import path
from . import views
app_name = 'payment_app'
urlpatterns = [
    
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('complete/',views.complete,name='complete'),
    path('purchase/<val_id>/<tran_id>/', views.purchase, name="purchase"),
    path('orders/', views.order_view, name="order"),
]