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
from django.template.loader import render_to_string

from taggit.models import Tag

from ajax_validation.views import validate_form
from ajax_validation.utils import render_json_response

from attachments.views import _do_ajax_upload, ajax_delete, ajax_change_descn 
from attachments.models import Attachment

from models import Timeline, get_all_timlines
from forms import TimelineForm, TlEventForm, CommentForm
from helper import event_to_dict, event_to_sdict

def index(request):
  return recommend(request)

def hot(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['pg'] = 'hot'
    ctx['timelines'] = get_all_timlines().order_by('-num_views')
    return render(request, template_name, ctx)

def last(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['pg'] = 'last'
    ctx['timelines'] = get_all_timlines().order_by('-updated_on')
    return render(request, template_name, ctx)

def recommend(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['pg'] = 'recommend'
    ctx['timelines'] = get_all_timlines().filter(rec=True).order_by('-rec_on')
    return render(request, template_name, ctx)

def random(request, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['pg'] = 'random'
    ctx['timelines'] = get_all_timlines().order_by('?')
    return render(request, template_name, ctx)


def tag(request, tag_name, template_name="timeline/timelines.html"):
    ctx = {}
    ctx['pg'] = 'tag'
    ctx['tag'] = get_object_or_404(Tag, name=tag_name)
    timelines = get_all_timlines().filter(tags__name__in=[tag_name]).order_by('-updated_on')
    ctx['timelines'] = timelines
    return render(request, template_name, ctx)

def tags(request, template_name="timeline/tags.html"):
    ctx = {}
    return render(request, template_name, ctx)

def full_screen(request, pk, template_name="timeline/t.html"):
    ctx = {}
    ctx['tl'] = get_object_or_404(Timeline, pk=pk)
    return render(request, template_name, ctx)

def detail(request, pk, template_name="timeline/detail.html"):
    ctx = {}
    timeline = get_object_or_404(Timeline, pk=pk)
    timeline.num_views += 1
    timeline.save()
    ctx['tl'] = timeline
    ctx['comments'] = timeline.comment_set.order_by('created_on')
    ctx['form'] = CommentForm()
    return render(request, template_name, ctx)

@login_required
def delete(request, pk):
    ctx = {}
    tl = get_object_or_404(Timeline, pk=pk)
    if tl.created_by != request.user:
        return HttpResponse(u'您没有权限执行该操作')
    tl.status = 'del'
    tl.save()
    return redirect('timeline_idx')

@login_required
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

@login_required
def edit(request, pk):
    ctx = {}
    template_name = 'timeline/form.html'
    timeline = get_object_or_404(Timeline, pk=pk)
    if timeline.created_by != request.user:
        return HttpResponse(u'您没有权限执行该操作')
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

def events_json_(request, pk):
    tl = Timeline.objects.get(pk=pk)
    t = {}
    timeline = { "type":"default" }
    t['timeline'] = timeline
    date = []
    timeline['date'] = date
    # cover
    events = tl.tlevent_set.filter(cover=True).order_by('startdate')
    if events.count():
        timeline.update(event_to_dict(events[0]))
    # date
    events = tl.tlevent_set.filter(cover=False).order_by('startdate')
    for e in events:
        date.append(event_to_dict(e))
    if not events.count():#if no events will get a js error.
        date.append({"startDate": "2012", 'headline': u'现在还没有任何事件，请先添加事件'})
    return render_json_response(t)

def events_sjson_(request, pk):
    tl = Timeline.objects.get(pk=pk)
    events = tl.tlevent_set.order_by('startdate')
    date = []
    for e in events:
        date.append(event_to_sdict(e))
    return render_json_response(date)

def addevent_(request, pk):
    timeline = get_object_or_404(Timeline, pk=pk)
    if timeline.created_by != request.user:
        return render_json_response({'valid': False})
    form, validate = validate_form(request, form_class=TlEventForm)
    if validate['valid']:
        event = form.save(commit=False)
        event.timeline = timeline
        event.save()
        timeline.update_num_events()
        timeline.update_updated_on()
        validate['data'] = event_to_sdict(event)
    return render_json_response(validate)

@login_required
def events(request, pk):
    ctx = {}
    tl = get_object_or_404(Timeline, pk=pk)
    ctx['tl'] = tl
    ctx['events'] = tl.tlevent_set.order_by('startdate')
    ctx['form'] = TlEventForm()
    return render(request, 'timeline/events.html', ctx)

def postcomment_(request, pk):
    timeline = get_object_or_404(Timeline, pk=pk)
    form, validate = validate_form(request, form_class=CommentForm)
    if not request.user.is_authenticated():
        return render_json_response({'valid': False})
    if validate['valid']:
        c = form.save(commit=False)
        c.timeline = timeline
        c.created_by = request.user
        c.save()
        timeline.update_num_replies()
        validate['html'] = render_to_string('timeline/inc_comment.html', { 'c': c })
    return render_json_response(validate)

def attach_upload(request, pk):
    template_name = "timeline/attach_upload.html"
    ctx = {}
    timeline = get_object_or_404(Timeline, pk=pk)
    ctx['tl'] = timeline
    return render(request, template_name, ctx)

@csrf_exempt
def attach_upload_(request, pk):
    if not request.user.is_authenticated():
        return render_json_response({'valid': False})
    timeline = get_object_or_404(Timeline, pk=pk)
    data = _do_ajax_upload(request)
    ret = {}
    if data['valid']:
        attach = Attachment.objects.get(pk=data['attachment']['id'])
        timeline.attachments.add(attach)
        ret['name'] = attach.org_filename
        ret['size'] = attach.file.size
        ret['url'] = attach.file.url
        ret['delete_url'] = "%s?id=%s" % (reverse('timeline_attach_delete_', args=[timeline.pk]), attach.pk)
    else:
        ret['error'] = u'上传失败'
    return render_json_response([ret, ]) 

@csrf_exempt
def attach_delete_(request, pk):
    attach = Attachment.objects.get(request.POST.get('id', 0) or request.GET.get('id', 0))
    if attach.created_by != request.user:
        return render_json_response({'valid': False})
    return ajax_delete(request)

@csrf_exempt
def attach_change_descn_(request, pk):
    attach = Attachment.objects.get(request.POST.get('id', 0) or request.GET.get('id', 0))
    if attach.created_by != request.user:
        return render_json_response({'valid': False})
    return ajax_change_descn(request)

def attachs_(request, pk):
    timeline = get_object_or_404(Timeline, pk=pk)
    attachs = timeline.attachments.order_by('-date_uploaded')
    data = []
    for a in attachs:
        data.append({'id': a.id, 'fn': a.org_filename, 
            'url': a.file.url, 'descn': a.description})
    return render_json_response(data) 

@login_required
def attachs(request, pk):
    template_name = "timeline/attachs.html"
    ctx = {}
    timeline = get_object_or_404(Timeline, pk=pk)
    ctx['tl'] = timeline
    attachs = timeline.attachments.order_by('-date_uploaded')
    ctx['attachs'] = attachs
    return render(request, template_name, ctx)
