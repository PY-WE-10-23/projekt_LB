from django.urls import path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('', views.index, name='index'),
    path('add_event/', views.add_event, name='add_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('remove_event/<int:event_id>/', views.remove_event, name='remove_event'),
    path('register_event/<int:event_id>/', views.register_event, name='register_event'),
    path('login/', auth.LoginView.as_view(template_name="members/login.html"), name='login'),
    path('logout/', auth.LogoutView.as_view(template_name="members/logout.html"), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('event_list/', views.event_list, name='event_list'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]
