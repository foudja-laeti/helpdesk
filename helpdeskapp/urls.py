from django.contrib import admin
from django.urls import path, include
from . import views


# Domaines
domaine_patterns = [
    path('', views.list_domaines, name='list_domaines'),
    path('add/', views.add_domaines, name='add_domaines'),
    path('update/<int:id>/', views.update_domaines, name='update_domaines'),
    path('delete/<int:id>/', views.delete_domaines, name='delete_domaines'),
]


# Utilisateurs
utilisateur_patterns = [
    path(
        '',
        views.list_utilisateurs,
        name='list_utilisateurs'),
    path(
        'add/',
        views.add_utilisateur,
        name='add_utilisateur'),
    path(
        'update/<int:id>/',
        views.update_utilisateur,
        name='update_utilisateur'),
    path(
        'delete/<int:id>/',
        views.delete_utilisateur,
        name='delete_utilisateur'),
    path(
        'detail/<int:id>/',
        views.detail_utilisateur,
        name='detail_utilisateur'),
    path(
        'role/<str:role>/',
        views.list_utilisateurs_by_role,
        name='list_utilisateurs_by_role'),
    path(
        'recherche/',
        views.search_utilisateurs,
        name='search_utilisateurs'),
]


# Demandes
demande_patterns = [
    path('', views.list_demandes, name='list_demandes'),
    path('add/', views.add_demande, name='add_demande'),
    path('update/<int:id>/', views.update_demande, name='update_demande'),
    path('delete/<int:id>/', views.delete_demande, name='delete_demande'),
    path('detail/<int:id>/', views.detail_demande, name='detail_demande'),
]


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentification
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Password Reset (NOUVEAU)
    path(
        'password-reset/',
        views.password_reset_request,
        name='password_reset_request'),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        views.password_reset_confirm,
        name='password_reset_confirm'),

    # Dashboards
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path(
        'dashboard/technicien/',
        views.dashboard_technicien,
        name='dashboard_technicien'),
    path('dashboard/client/', views.dashboard_client, name='dashboard_client'),

    # Modules
    path('domaine/', include((domaine_patterns, 'domaine'))),
    path('utilisateur/', include((utilisateur_patterns, 'utilisateur'))),
    path('demande/', include((demande_patterns, 'demande'))),
]
