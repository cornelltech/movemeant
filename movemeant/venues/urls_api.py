from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from venues import views

router = DefaultRouter()
router.register(r'cohorts', views.CohortViewSet)

urlpatterns = [
    url(r'^venues/logs/$', views.VenueLogAPIHandler.as_view()),
    url(r'^venues/checkin/$', views.VenueCheckinAPIHandler.as_view()),      
    url(r'^venues/reveal/$', views.VenueRevealAPIHandler.as_view()),

    url(r'^', include(router.urls)),
]