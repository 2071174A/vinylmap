__author__ = 'ross'
from django.conf.urls import patterns, url
from recordstoreapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
	url(r'^newreleases/$', views.new_releases, name='new_releases'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^search/', views.search, name = 'search'),
	url(r'^records/$', views.record_view, name='records'),
	url(r'^add_record/$', views.add_record, name='add_record'),
	url(r'^add_store/(?P<record_id>\w+)$', views.add_store, name='add_store'),
    )