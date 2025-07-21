from django.urls import path
from . import views

urlpatterns = [
    # URLs públicas
    path('', views.home, name='home'),
    path('ajuda/', views.help_page, name='help_page'),
    path('satisfaction/<int:pk>/', views.satisfaction_rating, name='satisfaction_rating'),

    # URLs administrativas
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('admin/reports/', views.reports, name='reports'),
    path('admin/update-status/<int:pk>/<str:status>/', views.update_status, name='update_status'),
    path('admin/update-priority/<int:pk>/<str:priority>/', views.update_priority, name='update_priority'),
    path('admin/delete/<int:pk>/', views.delete_feedback, name='delete_feedback'),
    path('admin/add-note/<int:pk>/', views.add_admin_note, name='add_admin_note'),
    path('admin/prioritize-all/', views.prioritize_all, name='prioritize_all'),
    path('admin/create-institution/', views.create_institution, name='create_institution'),
] 