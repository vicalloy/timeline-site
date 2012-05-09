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

from ajax_validation.views import validate_form
from ajax_validation.utils import render_json_response
#from ajax_validation.utils import render_string

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
            timeline = form.save(commit=False)
            timeline.created_by = request.user
            timeline.save()
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

def json_(request, pk):
    tl = Timeline.objects.get(pk=pk)
    t = { "timeline": {
        "headline":"The Kitchen Sink",
        "type":"default",
        "startDate":"2011,9,1",
        "text":"An example of the different kinds of stuff you can do.",
        "date": [ {
            "startDate":"2012,1,26",
            "headline":"Sh*t Politicians Say",
            "text":"<p>Sh*t Politicians Say landed just hours before Thursday night’s Republican presidential debate and stars actor Joe Leon. In true political fashion, his character rattles off common jargon heard from people running for office.</p><p>Do these ring a bell? Moral fiber, family values, trust me, three-point plan, earmarks, tough question, children are our future, Washington outsider, jobs, my opponent — all sound familiar.</p>",
            "asset":
            {
                "media":"http://youtu.be/u4XpeU9erbg",
                "credit":"",
                "caption":""
                }
            },
            {
                "startDate":"2012,1,10",
                "headline":"Sh*t Nobody Says",
                "text":"<p>Have you ever heard someone say “can I burn a copy of your Nickelback CD?” or “my Bazooka gum still has flavor!” Nobody says that.</p>",
                "asset":
                {
                    "media":"http://youtu.be/f-x8t0JOnVw",
                    "credit":"",
                    "caption":""
                    }
                },
            {
                "startDate":"2012,1,18",
                "headline":"Sh*t New Yorkers Say",
                "text":"",
                "asset":
                {
                    "media":"http://youtu.be/yRvJylbSg7o",
                    "credit":"",
                    "caption":"Directed and Edited by Matt Mayer, Produced by Seth Keim, Written by Eliot Glazer. Featuring Eliot and Ilana Glazer, who are siblings, not married."
                    }
                } ]
            } }
    return render_json_response(t)

def addevent_(request, pk):
    timeline = get_object_or_404(Timeline, pk=pk)
    form, validate = validate_form(request, form_class=TlEventForm)
    if validate['valid']:
        book = form.save(commit=False)
        book.timeline = timeline
        book.save()
        #validate['html'] = render_string(ROW_TMPL, {'o': book})
    return render_json_response(validate)
