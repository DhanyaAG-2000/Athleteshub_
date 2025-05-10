
from django.urls import path
from . import views

urlpatterns = [
    path('students-view/', views.StudentView.as_view(), name='students-view'),
    path('apply-events/', views.ApplyEventsview.as_view(), name='apply-events'),
    path('register-event/', views.StudentEventRegistrationView.as_view(), name='register-event'),
    path('registred-event-list/', views.RegisteredListView.as_view(), name='registred-event-list'),
    path('assign-winners/', views.AssignWinnersView.as_view(), name='assign-winners'),
    path('winners-list/', views.WinnersListView.as_view(), name='winners-list'),
   
]

 