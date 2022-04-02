from django.urls import path

from farmfoodapp import views

urlpatterns = [
    path('register-api/', views.register_api, name="register-api"),
    path('login-api/', views.login_api, name="login-api"),
    path('register/', views.register_view, name='register-view'),
    path('login/', views.login_view, name='login-view'),
    path('forget-password/', views.forget_password_view, name='forget-password'),
    path('reset/<str:token>', views.reset_password_view, name='reset-password'),
    path('verify/<str:token>', views.verify_reg_email, name="verify_reg_email"),
    path('reset-password-api/', views.reset_password_api, name="reset-password-api"),

]
