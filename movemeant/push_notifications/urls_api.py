from django.conf.urls import url

import views

urlpatterns = [
    url(r'^devices/create/$', views.DeviceCreateView.as_view()),
]
