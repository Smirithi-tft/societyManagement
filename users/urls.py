from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sign-up/', views.user_signup, name='user-signup'),
    path('login/', views.user_login, name='user-login'),
    path('verify_otp', views.verify_otp, name='verify-otp'),
    path('send_email/', views.send_email, name='send-email'),
    path('verify_email/', views.verify_email, name='verify-email'),
    path('reset-password/', views.password_reset, name='password-reset'),
    path('confirm-password/', views.confirm_password, name='confirm-password'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
