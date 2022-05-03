from django.urls import path
from . import views

urlpatterns = [
    # path('user/list/', views.user_list),
    # path('user/info/', views.user_info),
    # path('user/add/', views.user_add),
    # path('user/delete/', views.user_delete),

    path('', views.home),

    # 医院用户管理
    path('hospital/list/', views.hospital_list),
    path('hospital/add/', views.hospital_add),
    path('hospital/delete/', views.hospital_delete),
    path('hospital/<int:nid>/edit/', views.hospital_edit),

    # 药品管理
    path('hospital/department/drogs/list', views.drogs_list),
    path('hospital/department/drogs/add/', views.drogs_add),
    path('hospital/department/drogs/delete/', views.drogs_delete),
    path('hospital/department/drogs/<int:nid>/edit/', views.drogs_edit),
    # 设备管理
    path('hospital/department/devices/list/', views.devices_list),
    path('hospital/department/devices/add/', views.devices_add),
    path('hospital/department/devices/delete/', views.devices_delete),
    path('hospital/department/devices/<int:nid>/edit/', views.devices_edit),

    # 管理员管理
    path('manageadmin/', views.admin_list),
    path('manageadmin/add/', views.admin_add),
    path('manageadmin/delete/', views.admin_delete),
    path('manageadmin/<int:nid>/edit/', views.admin_edit),
    path('manageadmin/<int:nid>/reset/', views.admin_pwd_reset),

]
