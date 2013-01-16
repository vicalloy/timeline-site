from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from userena.contrib.umessages import views as messages_views
from profiles.forms import BsComposeForm

from timeline.sitemaps import sitemaps

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'timeline.views.index', name='idx'),
    url(r'^accounts/', include('profiles.urls')),
    url(r'^messages/compose/$',
        messages_views.message_compose,
        {'compose_form': BsComposeForm},
        name='userena_umessages_compose'),
    url(r'^messages/compose/(?P<recipients>[\+\.\w]+)/$',
        messages_views.message_compose,
        {'compose_form': BsComposeForm},
        name='userena_umessages_compose_to'),
    url(r'^messages/reply/(?P<parent_id>[\d]+)/$',
        messages_views.message_compose,
        {'compose_form': BsComposeForm},
        name='userena_umessages_reply'),
    url(r'^messages/', include('userena.contrib.umessages.urls')),
    url(r'^p/(?P<username>[\.\w]+)/$',
       'profiles.views.profile_detail',
       name='userena_profile_detail'),
    #url(r'^attachments/', include('attachments.urls')),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), 
      name="timeline_about"),
    url(r'^faq/$', TemplateView.as_view(template_name="faq.html"),
      name="timeline_faq"),
    url(r'^', include('timeline.urls')),
)

urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
