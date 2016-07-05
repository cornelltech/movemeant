from django.conf.urls import url, include

from venues import views

urlpatterns = [
    url(r'^venues/checkin/$', views.VenueCheckinAPIHandler.as_view()),      
]