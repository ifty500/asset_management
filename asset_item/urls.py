from django.urls import path
from .import views

urlpatterns = [

    path('register/', views.registerPage,name = 'register'),
    path('login/', views.loginPage,name = 'login'),
    path('logout/', views.logoutUser,name = 'logout'),


    path('', views.home, name ='home'),
    path('company_entry', views.company_entry, name ='company_entry'),
    path('company_list', views.company_list, name ='company_list'),
    path('company_list/<str:pk>/', views.company_edit, name='company_edit'),
    path('company_list/<str:pk>/delete/', views.company_delete, name='company_delete'),
    
    path('item_entry', views.item_entry, name ='item_entry'),
    path('item_list', views.item_list, name ='item_list'),
    path('item_list/<str:pk>/', views.item_edit, name='item_edit'),
    path('item_list/<str:pk>/delete/', views.item_delete, name='item_delete'),

    path('employee_entry', views.employee_entry, name ='employee_entry'),
    path('employee_list', views.employee_list, name ='employee_list'),
    path('employee_list/<str:pk>/', views.employee_edit, name='employee_edit'),
    path('employee_list/<str:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('employee_upload', views.employee_upload, name='employee_upload'), #uplaod employee

    path('department_entry', views.department_entry, name ='department_entry'),
    path('department_list', views.department_list, name ='department_list'),
    path('department_list/<str:pk>/', views.department_edit, name='department_edit'),
    path('department_list/<str:pk>/delete/', views.department_delete, name='department_delete'),


    path('ajax/load-departments/', views.load_department, name='ajax_load_departments'),
    path('ajax/load-employees/', views.load_employees, name='ajax_load_employees'),

]

