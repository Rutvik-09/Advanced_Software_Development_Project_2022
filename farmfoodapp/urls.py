from django.urls import path

from farmfoodapp import views

urlpatterns = [
    path('register-api/', views.register_api, name="register-api"),
    path('login-api/', views.login_api, name="login-api"),
    path('register/', views.register_view, name='register-view')
]
