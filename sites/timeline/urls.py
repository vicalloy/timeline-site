from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from timeline import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='timeline_idx'),
    url(r'^t/(?P<pk>\d+)/$', views.detail, name='timeline_detail'),
    url(r'^t/$', TemplateView.as_view(template_name='base_site.html')),
)
