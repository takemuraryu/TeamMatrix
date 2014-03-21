from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RequirementTracker.views.home', name='home'),
    # url(r'^RequirementTracker/', include('RequirementTracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    #url(r'^rango/', include('rango.urls')),
    url(r'^', include('RT_MW.urls')),
    url(r'^user_interface/', include('RT_MW.urls')),
    #url(r'^user_interface/create_project/', include('RT_MW.urls')),
    url(r'^project_detail/', include('RT_MW.urls')),
    #url(r'^project_detail/create_todo_attr', include('RT_MW.urls')),
    #url(r'^project_detail/detail_todo_attr', include('RT_MW.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
