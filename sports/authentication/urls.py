from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

    path('login/',views.LoginView.as_view(),name="login"),
    path('logout/',views.LogoutView.as_view(),name="logout"),
    path("password-reset/", views.ForgotPasswordView.as_view(), name="password_reset"),  #  Matches password_reset.html
    path("password-reset/<uidb64>/<token>/", views.ConfirmPasswordResetView.as_view(), name="password_reset_confirm"),  #  Matches password_reset_confirm.html


             ]  







