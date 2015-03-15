from django.conf.urls import patterns, include, url
from django.contrib import admin
from recordstoreapp import views
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vinylmap_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^vinylmaps/', include('recordstoreapp.urls')),
    #if user types in ourwebsite.com they are redirected to ourwebsiteDomain/vinylmaps/
    url(r'^$', views.baseRedirect, name='baseRedirect'),

)

