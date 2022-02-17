from django.urls import path

from farmfoodapp import views

urlpatterns = [
    path('register-api/', views.register_api, name="register-api"),
    path('login-api/', views.login_api, name="login-api")
]
