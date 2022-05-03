from django.urls import path
from . import views

urlpatterns = [
    # 医药公司处理
    path('devices_company/list', views.devices_company_list),
    path('devices_company/add/', views.devices_company_add),
    path('devices_company/delete/', views.devices_company_delete),
    path('devices_company/<int:nid>/edit/', views.devices_company_edit),

    # 药品处理
    path('devices_company/devices_provide/list', views.devices_provide_list),
    path('devices_company/devices_provide/add/', views.devices_provide_add),
    path('devices_company/devices_provide/delete/', views.devices_provide_delete),
    path('devices_company/devices_provide/<int:nid>/edit/', views.devices_provide_edit),

    path('devices_company/devices_provide/<int:nid>/user/', views.devices_provide_user_edit),
    path('devices_company/devices_provide/<int:nid>/evaluate/', views.devices_provide_evaluate),
    path('devices_company/devices_provide/<int:nid>/<int:eid>/evaluate/list/', views.devices_provide_evaluate_list),
]