
from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.DashboardView.as_view(),name='dashboard'),

    path('contact/',views.ContactView.as_view(),name='contact'),

    path('adminview/',views.AdminView.as_view(),name='adminview'),

    path('registration/',views.RegistrationView.as_view(),name="registration"),

    path('user-management/',views.UserListView.as_view(),name='user-management'),

    path('user-detail/<str:uuid>/',views.UserDetailView.as_view(),name='user-detail'),

    path('user-delete/<str:uuid>/',views.UserDeleteView.as_view(),name='user-delete'),
    
    path('update/', views.UserUpdateView.as_view(), name='user-update'),

    path('success/',views.SuccessfullyregisteredView.as_view(),name='success'),
    
    path('compaining/',views.EventCompainingView.as_view(),name='compaining'),






    

   
]