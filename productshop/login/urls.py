from django.urls import path
from . views import *
from django.contrib.auth.views import PasswordResetView, \
    PasswordResetDoneView, \
    PasswordResetConfirmView, \
    PasswordResetCompleteView, \
    PasswordChangeView, \
    PasswordChangeDoneView

from main.views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='login/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='login/password_reset_done.html'), name='password_reset_done'),
    path('reset<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='login/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='login/password_reset_complete.html'), name='password_reset_complete'),
    path('password-change/', PasswordChangeView.as_view(template_name='login/password_change_form.html'), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='login/password_change_done.html'), name='password_change_done'),
]
