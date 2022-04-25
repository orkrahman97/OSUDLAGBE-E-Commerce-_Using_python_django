from django.urls import path 
from . import views
app_name = 'login_app'



urlpatterns = [
    path('',views.signup_user,name='signup'),  
    path('sign_up/',views.signup_user,name='signup'), 
    path('login/',views.login_user,name='login'), 
    path('logout/',views.logout_user,name='logout'),
    path('profile/',views.user_profile,name='user_profile'),  
]