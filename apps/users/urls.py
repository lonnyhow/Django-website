from django.urls import path
from . import views


app_name = 'users'

# {% url 'users:название_ссылки' %}

# users/login/

urlpatterns = [
    path('login/', views.login_user, name='login-user'),
    path('registration/', views.register_user, name='register-user'),
    path('logout/', views.logout_user, name='logout-user'),
    path('profile/<str:username>/', views.show_author_profile, name='profile')
]
