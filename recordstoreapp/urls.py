__author__ = 'ross'
from django.conf.urls import patterns, url
from recordstoreapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    #url(r'^backcatalogue/$', views.backCat, name='genrebackcatalogue'),
    #url(r'^future/$', views.forthcoming, name='genreforthcoming'),
	url(r'^newreleases/$', views.new_releases, name='new_releases'),
    #url(r'^genre/(?P<genre_name_url>[\w\-]+)/backcatalogue/$', views.backCat, name='genrebackcatalogue'),
    #url(r'^genre/(?P<genre_name_url>[\w\-]+)/future/$', views.forthcoming, name='genreforthcoming'),
    #url(r'^genre/(?P<genre_name_url>[\w\-]+)/new/$', views.new_releases, name='genrenewreleases'),
    #url(r'^genre/(?P<genre_name_url>[\w\-]+)/$', views.genre, name='genre'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^search/', views.search, name = 'search'),
	url(r'^records/$', views.record_view, name='records'),
    )