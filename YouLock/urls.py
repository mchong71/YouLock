from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YouLock.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'lock.views.index', name='index'),
    url(r'^share/$', 'lock.views.share', name='share'),
    url(r'^listen/$', 'lock.views.listen', name='listen'),
    url(r'^admin/', include(admin.site.urls)),
)
