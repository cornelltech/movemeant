from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from venues import views

router = DefaultRouter()
router.register(r'cohorts', views.CohortViewSet)

urlpatterns = [
    url(r'^my/venues/logs/$', views.VenueMineCohortLogAPIHandler.as_view()),

    url(r'^venues/logs/$', views.VenueCohortLogAPIHandler.as_view()),
    url(r'^venues/search/$', views.VenueSearchAPIHandler.as_view()),
    url(r'^venues/checkin/$', views.VenueCheckinAPIHandler.as_view()),      
    url(r'^venues/reveal/$', views.VenueRevealAPIHandler.as_view()),

    url(r'^', include(router.urls)),
]