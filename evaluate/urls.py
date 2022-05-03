# 交易评估
from django.urls import path
from . import views
urlpatterns = [
    path('evaluate/', views.evaluate_insurance)
]
