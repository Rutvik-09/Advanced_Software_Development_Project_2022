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
    path('', views.home_page, name="home-page"),
    path('add-product/', views.add_product_view, name="add-product"),
    path('onboard-vendor/', views.onboard_vendor_view_api, name="onboard-vendor"),
    path('view-products/', views.view_products, name="view_products"),
    path('edit/<int:prod_id>', views.edit_product, name="edit-product"),
]
