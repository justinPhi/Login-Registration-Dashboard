from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index),
        url(r'^dashboard$', views.displayDashboard),
        url(r'^register$', views.register),
        url(r'^login$', views.login),
        url(r'^index$', views.index),
        ]
