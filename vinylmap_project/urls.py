from django.conf.urls import patterns, include, url
from django.contrib import admin
from recordstoreapp import views
from django.conf import settings


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('recordstoreapp.urls')),
)

