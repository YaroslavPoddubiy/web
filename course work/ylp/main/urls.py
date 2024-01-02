from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('landing/', views.landing, name='landing'),
    path('container/', views.container, name='container'),
    path('info/', views.info, name='info'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('del_from_cart/', views.del_from_cart, name='del_from_cart'),
    path('del_feedback/', views.del_feedback, name='del_feedback')
]
