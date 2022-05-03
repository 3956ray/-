from django.urls import path
from . import views

urlpatterns = [
    # 医药公司处理
    path('drogs_company/list', views.drogs_company_list),
    path('drogs_company/add/', views.drogs_company_add),
    path('drogs_company/delete/', views.drogs_company_delete),
    path('drogs_company/<int:nid>/edit/', views.drogs_company_edit),

    # 药品处理
    path('drogs_company/drogs_provide/list', views.drogs_provide_list),
    path('drogs_company/drogs_provide/add/', views.drogs_provide_add),
    path('drogs_company/drogs_provide/delete/', views.drogs_provide_delete),
    path('drogs_company/drogs_provide/<int:nid>/edit/', views.drogs_provide_edit),

    path('drogs_company/drogs_provide/<int:nid>/user/', views.drogs_provide_user_edit),
    path('drogs_company/drogs_provide/<int:nid>/evaluate/', views.drogs_provide_evaluate),
    path('drogs_company/drogs_provide/<int:nid>/<int:eid>/evaluate/list/', views.drogs_provide_evaluate_list),
]
