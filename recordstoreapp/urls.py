__author__ = 'ross'
from django.conf.urls import patterns, url
from recordstoreapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^backcatalogue/$', views.backCat, name='genrebackcatalogue'),
    url(r'^future/$', views.forthcoming, name='genreforthcoming'),
    url(r'^new/$', views.newReleases, name='genrenewreleases'),
    url(r'^(?P<genre_name_slug>[\w\-]+)/backcatalogue/$', views.backCat, name='genrebackcatalogue'),
    url(r'^(?P<genre_name_slug>[\w\-]+)/future/$', views.forthcoming, name='genreforthcoming'),
    url(r'^(?P<genre_name_slug>[\w\-]+)/new/$', views.newReleases, name='genrenewreleases'),
    url(r'^(?P<genre_name_slug>[\w\-]+)/$', views.genre, name='genre'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^search/(?P<search_slug>[\w\-]+)', views.search, name = 'search'),
    )