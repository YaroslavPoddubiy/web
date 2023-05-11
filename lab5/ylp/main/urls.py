from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('container/', views.container, name='container'),
    path('info/', views.info, name='info'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login')
]
