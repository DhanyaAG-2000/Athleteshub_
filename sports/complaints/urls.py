from django.urls import path
from . import views


urlpatterns = [
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),  # URL for the feedback form submission
    path('tnku/', views.FeedbackSuccessView.as_view(), name='tnku'),  # URL for the feedback success page
    path('feedback-list/', views.FeedbackListView.as_view(), name='feedback-list'),  # URL for the feedback list page
]
