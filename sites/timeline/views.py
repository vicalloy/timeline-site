# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from models import Timeline, Recommend

def index(request):
  return recommend(request)

def __timeline(request, template_name="lbforum/recent.html"):
    ctx = {}
    timelines = Timeline.objects.all()
    #timelines = timelines.filter(updated_on__lt = '')
    #timelines = timelines.order_by('num_views')
    timelines = timelines.order_by('updated_on')
    #TODO TAG.NEW.recommend, LAST WEEK, LAST MONTH.
    ctx['timelines'] = timelines
    return render(request, template_name, ctx)

def recommend(request, template_name="timeline/recommend.html"):
    ctx = {}
    recommends = Recommend.objects.all()
    recommends = recommends.order_by('-updated_on')
    #TODO TAG.NEW.recommend, LAST WEEK, LAST MONTH.
    ctx['recommends'] = recommends
    return render(request, template_name, ctx)

def detail(request, pk, template_name="timeline/detail.html"):
    ctx = {}
    ctx['tl'] = get_object_or_404(Timeline, pk=pk)
    return render(request, template_name, ctx)
