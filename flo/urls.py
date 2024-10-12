from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:id>/', views.view_company, name='view_company'),
    path('owing', views.owing, name='owing'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit/<int:id>/', views.edit, name='edit'),
]