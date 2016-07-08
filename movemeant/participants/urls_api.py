from django.conf.urls import url, include

from participants import views

urlpatterns = [
    url(r'^me/$', views.MeAPIHandler.as_view()),
    url(r'^participants/add/$', views.UserCreateAPIHandler.as_view()),
    url(r'^cohorts/affiliate/$', views.AffiliateUserWithRegionAPIHandler.as_view()),
]