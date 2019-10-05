from django.urls import path

from . import views

app_name = 'vcode_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('send_vcode/', views.send_vcode, name='send_mail_vcode'),
    path('validate_vcode/', views.validate_vcode, name='validate_mail_vcode'),
]
