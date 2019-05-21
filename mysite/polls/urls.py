from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.read_file, name='read_file'),
]