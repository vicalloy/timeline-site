# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from models import Timeline
from forms import TimelineForm, TlEventForm

def index(request):
  return recommend(request)

def hot(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['pg'] = 'hot'
    ctx['timelines'] = Timeline.objects.order_by('-num_views')
    return render(request, template_name, ctx)

def last(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['pg'] = 'last'
    ctx['timelines'] = Timeline.objects.order_by('-updated_on')
    return render(request, template_name, ctx)

def recommend(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['pg'] = 'recommend'
    ctx['timelines'] = Timeline.objects.filter(rec=True).order_by('-rec_on')
    return render(request, template_name, ctx)

def random(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['pg'] = 'random'
    ctx['timelines'] = Timeline.objects.order_by('?')
    return render(request, template_name, ctx)

def full_screen(request, pk, template_name="timeline/t.html"):
    ctx = {}
    ctx['tl'] = get_object_or_404(Timeline, pk=pk)
    return render(request, template_name, ctx)

def detail(request, pk, template_name="timeline/detail.html"):
    ctx = {}
    ctx['tl'] = get_object_or_404(Timeline, pk=pk)
    ctx['form'] = TlEventForm()
    return render(request, template_name, ctx)

def new(request):
    ctx = {}
    template_name = 'timeline/form.html'
    form = TimelineForm()
    if request.method == "POST":
        form = TimelineForm(request.POST, request.FILES)
        if form.is_valid():
            timeline = form.save()
            return redirect('timeline_detail', timeline.pk)
    ctx['form'] = form
    return render(request, template_name, ctx)

def edit(request, pk):
    ctx = {}
    template_name = 'timeline/form.html'
    timeline = get_object_or_404(Timeline, pk=pk)
    ctx['tl'] = timeline
    form = TimelineForm(instance=timeline)
    if request.method == "POST":
        form = TimelineForm(request.POST, request.FILES, instance=timeline)
        if form.is_valid():
            form.save()
            messages.info(request, u'成功编辑')
            return redirect('timeline_detail', timeline.pk)
    ctx['form'] = form
    ctx['tl'] = timeline
    return render(request, template_name, ctx)

def load_form(request, form_class):
    pass

def load(request, pk):
    tl = Timeline.objects.get(pk=pk)
    t = {
            "id": 'id-%s' % tl.pk,
            "title": tl.title,
            "focus_date": "2001-01-01 12:00:00",
            "initial_zoom": "43",
            "timezone": "-07:00"}
    t['events'] = [
            {
                "id":"jshist-self",
                "title": "Self",
                "description":"Self, one of the inspirations for Javascript's simplicity, is created at Xerox PARC ",
                "startdate": "1986-01-01 12:00:00",
                "importance":"40",
                "date_display":"none",
                "icon":"flag_green.png"
                },
            
            {
                "id":"jshist-01",
                "title": "Mocha - Live Script",
                "description": "<img src='img/eich.jpg' style='float:left;margin-right:8px;margin-bottom:8px'>JavaScript was originally developed by Brendan Eich of Netscape under the name Mocha. LiveScript was the official name for the language when it first shipped in beta releases of Netscape Navigator 2.0 in September 1995",
                "startdate": "1995-05-01 12:00:00",
                "date_limit":"ho",
                "link":"http://en.wikipedia.org/wiki/JavaScript",
                "importance":"40",
                "icon":"flag_green.png"
                },

            {
                "id": "jshist-02",
                "title": "JavaScript is Born",
                "description": "LiveScript is Renamed JavaScript in a joint announcement with Netscape and Sun Microsystems",
                "startdate": "1995-12-04 12:00:00",
                "enddate": "1995-12-04",
                "date_display": "day",
                "link": "http: //en.wikipedia.org/wiki/JavaScript",
                "importance": 50,
                "icon":"triangle_orange.png"
                },
            {
                "id":"jshist-09",
                "title": "jQuery",
                "description": "Released in January 2006 at BarCamp NYC by John Resig",
                "startdate": "2005-12-01 12:00:00",
                "enddate": "2005-12-01 12:00:00",
                "link":"http://jquery.com/",
                "importance":"40",
                "image":"img/jquery.jpg",
                "image_class":"above",
                "icon":"triangle_green.png"
                },
            {
                "id":"jshist-dry",
                "title": "The Bad Rap Years",
                "description": "Of Javascript's initial insinuation into browsers, WWW founder Robert Cailliau said, 'the programming-vacuum filled itself with the most horrible kluge in the history of computing: Javascript.' But now JS is 'hawt' and its clay-like flexibility makes it enjoyable, inspiring more artistry and cleverness than other languages.",
                "startdate": "1998-01-01 12:00:00",
                "enddate": "2004-01-01 12:00:00",
                "date_limit":"mo",
                "span_color":"#FF0000",
                "link":"http://en.wikipedia.org/wiki/JavaScript",
                "importance":"52",
                "icon":"none"
                },
            
            ]
    return HttpResponse(simplejson.dumps([t]), mimetype='text/html')#application/json
