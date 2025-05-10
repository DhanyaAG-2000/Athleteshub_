
from django.urls import path

from .import views


urlpatterns = [

    path('event/', views.SportsEventView.as_view(), name='event'),

    path('event-list/', views.EventList.as_view(), name='event-list'),

    path('event-register/', views.SportsEventRegisteredView.as_view(), name='event-register'),

    path('event-update/<int:pk>/', views.SportsEventUpdateView.as_view(), name='event-update'),
  
    path('events/delete/<int:pk>/',views. SportsEventDeleteView.as_view(), name='event-delete'),
]
