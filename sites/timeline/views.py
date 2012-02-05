# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from models import Timeline

def index(request):
  return recommend(request)

def hot(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['timelines'] = Timeline.objects.order_by('-num_views')
    return render(request, template_name, ctx)

def last(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['timelines'] = Timeline.objects.order_by('-updated_on')
    return render(request, template_name, ctx)

def recommend(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['timelines'] = Timeline.objects.filter(rec=True).order_by('-rec_on')
    return render(request, template_name, ctx)

def detail(request, pk, template_name="timeline/detail.html"):
    ctx = {}
    ctx['tl'] = get_object_or_404(Timeline, pk=pk)
    return render(request, template_name, ctx)
