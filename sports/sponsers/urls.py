from django.urls import path

from .import views

urlpatterns = [
    path('sponsers-view/',views.SponsersView.as_view(),name='sponsers-view'),
    path('sponsor-list/',views.SponsorsListView.as_view(),name='sponsor-list'),
    path('athletes-view-list/',views.SponsorAthleteListView.as_view(),name='athletes-view-list'),
    path('sponsor-company/', views.SponsorCompanyView.as_view(), name='sponsor-company'), 
    path("pending-list/",views.StudentRequestCompanyView.as_view(),name="pending-list"),
    path('send-request/<int:sponsor_id>/', views.SendSponsorshipRequestView.as_view(), name='send-request'),
    path('requests/',views.SponsorRequestManageView.as_view(), name='sponsor-manage-requests'),
    path('send-request-success/',views.RequestsendsuccessfullyView.as_view(), name='send-request-success'),
    path('send-request-fail/',views.RequestsendFailView.as_view(), name='send-request-fail'),
    path('sponsorship-request/accept/<int:request_id>/', views.ChangeRequestStatusView.as_view(), name='accept-request'),
    path('sponsorship-request/reject/<int:request_id>/', views.ChangeRequestStatusView.as_view(), name='reject-request'),
    path('admin-request-view/',views.AdminSponsorshipOverviewView.as_view(),name='admin-request-view'),
    path('query/',views.queryView.as_view(),name='query'),
 
    
    
   
]

 
   

    
