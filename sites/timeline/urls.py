from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from timeline import views

urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name='index.html')),
    url('^t/$', TemplateView.as_view(template_name='base_site.html')),
)
