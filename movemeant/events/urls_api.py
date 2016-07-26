from django.conf.urls import url, include

from events import views

urlpatterns = [
    url(r'^events/$', views.EventCreateAPIHandler.as_view()),
]