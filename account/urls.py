from django.urls import path
from . import views

urlpatterns = [
    # 登录注册
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
]
