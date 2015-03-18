__author__ = 'ross'
from django.conf.urls import patterns, url
from recordstoreapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^backcatalogue/$', views.backCat, name='genrebackcatalogue'),
    url(r'^future/$', views.forthcoming, name='genreforthcoming'),
    url(r'^new/$', views.newReleases, name='genrenewreleases'),
    url(r'^genre/(?P<genre_name_url>[\w\-]+)/backcatalogue/$', views.backCat, name='genrebackcatalogue'),
    url(r'^genre/(?P<genre_name_url>[\w\-]+)/future/$', views.forthcoming, name='genreforthcoming'),
    url(r'^genre/(?P<genre_name_url>[\w\-]+)/new/$', views.newReleases, name='genrenewreleases'),
    url(r'^genre/(?P<genre_name_url>[\w\-]+)/$', views.genre, name='genre'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^search/', views.search, name = 'search'),
    )