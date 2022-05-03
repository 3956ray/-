from django.urls import path
from . import views

urlpatterns=[
# 患者管理
    path('hospital/patient/', views.patient_list),
    path('hospital/patient/add/', views.patient_add),
    path('hospital/patient/delete/', views.patient_delete),
    path('hospital/patient/<int:nid>/edit/', views.patient_edit),

    # 患者病史管理
    path('hospital/patient/history/', views.patient_history_list),
    path('hospital/patient/history/add', views.patient_history_add),
    path('hospital/patient/history/delete/', views.patient_history_delete),
    path('hospital/patient/history/<int:nid>/edit/', views.patient_history_edit),
    path('hospital/patient/<int:nid>/history/', views.patient_user_list),
]