from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_view

# handler403 = 'authentication_app.views.permission_denied'

urlpatterns=[
    path('',views.home_page,name="home"),
    path('register',views.register_page,name="register"),
    path('email_verify',views.email_verify,name="email_verify"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('password_change',auth_view.PasswordChangeView.as_view(template_name="auth_app/change_password.html",success_url="password_change/done"),name="password_change"),
    path('password_change/done',views.changed_password,name="password_change_done"),
    path('password_reset/',auth_view.PasswordResetView.as_view(template_name="auth_app/registration/password_reset_form.html"),name="password_reset"),
    path('password_reset/done',auth_view.PasswordResetDoneView.as_view(template_name="auth_app/registration/password_reset_done.html"),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name="auth_app/registration/password_reset_confirm.html"),name="password_reset_confirm"),
    path('password_reset_complete/done',auth_view.PasswordResetCompleteView.as_view(template_name="auth_app/registration/password_reset_complete.html"),name="password_reset_complete"),
    path('update_user_profile',views.update_user_profile,name="update_user_profile"),
    path('user_profile_page',views.user_profile_page,name="user_profile_page"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('edit_profile/<int:user_id>',views.edit_profile,name="edit_profile"),
    path('delete_profile/<int:user_id>',views.delete_profile,name="delete_profile"),
    # path('403',views.permission_denied,name="permission_denied"),
    ]