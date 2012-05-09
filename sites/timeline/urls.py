from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from timeline import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='timeline_idx'),
    url(r'^hot/$', views.hot, name='timeline_hot'),
    url(r'^recommend/$', views.recommend, name='timeline_recommend'),
    url(r'^last/$', views.last, name='timeline_last'),
    url(r'^random/$', views.random, name='timeline_random'),
    url(r'^t/(?P<pk>\d+)/fs/$', views.full_screen, name='timeline_full_screen'),
    url(r'^t/(?P<pk>\d+)/$', views.detail, name='timeline_detail'),
    url(r'^t/(?P<pk>\d+)/edit/$', views.edit, name='timeline_edit'),
    url(r'^t/(?P<pk>\d+)/json_/$', views.json_, name='timeline_json'),
    url(r'^t/$', TemplateView.as_view(template_name='base_site.html')),
    url(r'^t/new/$', views.new, name='timeline_new'),
    url(r'^t/(?P<pk>\d+)/addevent_/$', views.addevent_, name='timeline_addevent_'),
)

urlpatterns += patterns('',
)
