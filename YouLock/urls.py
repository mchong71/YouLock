from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YouLock.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'lock.views.index', name='index'),
    url(r'^login/$', 'lock.views.login', name='login'),
    url(r'^logout/$', 'lock.views.logout', name='logout'),
    url(r'^authenticate/$', 'lock.views.authenticate'),
    url(r'^toggle/$', 'lock.views.toggle'),
    url(r'^share/$', 'lock.views.share', name='share'),
    url(r'^delete/$', 'lock.views.delete', name='delete'),
    url(r'^listen/$', 'lock.views.listen', name='listen'),
    url(r'^admin/', include(admin.site.urls)),
)
