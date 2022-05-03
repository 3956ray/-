from django.urls import path
from . import views

urlpatterns = [
    # 保险公司处理   
    path('insurance/list', views.insurance_list),
    path('insurance/add/', views.insurance_add),
    path('insurance/delete/', views.insurance_delete),
    path('insurance/<int:nid>/edit/', views.insurance_edit),

    # 保险处理
    path('insurance/insurance_provide/list', views.insurance_provide_list),
    path('insurance/insurance_provide/add/', views.insurance_provide_add),
    path('insurance/insurance_provide/delete/', views.insurance_provide_delete),
    path('insurance/insurance_provide/<int:nid>/edit/', views.insurance_provide_edit),

    path('insurance/<int:nid>/user/', views.insurance_user_list),
    path('insurance/<int:nid>/evaluate/', views.insurance_evaluate),
    path('insurance/<int:nid>/<int:eid>/evaluate/list', views.insurance_evaluate_list),
    # path('insurance/evaluate/delete/', views.insurance_evaluate_delete),
]
