from django.urls import path
from . import views

urlpatterns=[
# 科室管理
    path('hospital/department/', views.department_list),
    path('hospital/department/add/', views.department_add),
    path('hospital/department/delete/', views.department_delete),
    path('hospital/department/<int:nid>/edit/', views.department_edit),
]