# -*- coding: UTF-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from userena.utils import generate_sha1
from attachments.models import Attachment
from easy_thumbnails.fields import ThumbnailerImageField
from taggit.managers import TaggableManager

def upload_to_cover(instance, filename):
    salt, hash = generate_sha1(instance.id)
    extension = filename.split('.')[-1].lower()
    return '%(path)s%(hash)s.%(extension)s' % {'path': 'cover/',
                                               'hash': hash[:10],
                                               'extension': extension}

class Timeline(models.Model):
    STATUS_CHOICES = (('draft', u'草稿'), 
            ('pub', u'发布'),
            ('del', u'删除'))
    title = models.CharField(u'标题', max_length=30)
    cover = ThumbnailerImageField(u'封面',
            blank=True,
            upload_to=upload_to_cover,
            resize_source={'size': (140,140), 'crop': 'smart'},
            help_text=u'封面图片')
    tags = TaggableManager(blank=True)
    intro = models.TextField(u'简介', max_length=30,
            help_text=u"""支持Markdown格式。 
            <a href="http://markdown.tw/" target="_blank">Markdown格式说明</a>""")
    focus_date = models.CharField(u'初始日期', max_length=30, null=True, blank=True)
    attachments = models.ManyToManyField(Attachment, blank = True)
    status = models.CharField(u"发布状态", max_length=16, default='draft', choices=STATUS_CHOICES)

    num_events = models.IntegerField(u'事件数', default=0)
    num_views = models.IntegerField(u'浏览次数', default=0)
    num_replies = models.PositiveSmallIntegerField(u'回复数', default=0)

    rec = models.BooleanField(u'推荐', default=False)
    rec_on = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __unicode__(self):
        return self.title

    class Meta:
        permissions = (
            ('admin', u'管理员'),#暂不使用，时间线的创建者就是管理员
            ('collaborator', u'协作者'),
        )

    def update_updated_on(self, commit=True):
        self.updated_on = datetime.now()
        if commit:
            self.save()

    def update_num_events(self, commit=True):
        self.num_events = self.tlevent_set.count()
        if commit:
            self.save()

    def update_num_replies(self, commit=True):
        self.num_replies = self.comment_set.count()
        if commit:
            self.save()

    def get_cover_url(self):
        if self.cover:
            return self.cover.url
        return getattr(settings, 'TL_COVER_URL', None)

    @models.permalink
    def get_absolute_url(self):
        return ('timeline_detail', (self.pk, ))

    def can_edit(self, user):
        return user.has_perm('collaborator', self) or \
                self.created_by == user

def get_all_timlines():
    return Timeline.objects.filter(status='pub')

class TlEvent(models.Model):
    timeline = models.ForeignKey(Timeline)
    title = models.CharField(u'标题', max_length=30)
    startdate = models.CharField(u'开始日期', max_length=32, 
            help_text=u"支持的日期格式：, yyyy-mm-dd(2012-12-20)、yyyy(2012)")
    enddate = models.CharField(u'结束日期', max_length=32, blank=True, null=True, 
            help_text=u"支持的日期格式：, yyyy-mm-dd(2012-12-20)、yyyy(2012)")
    text = models.TextField(u'详细说明', blank=True, null=True, 
            help_text=u"""支持Markdown格式，
            <a href="http://markdown.tw/" target="_blank">Markdown格式说明</a>""")

    media = models.TextField(u'媒体', blank=True, null=True, help_text=u'可以是文字、图片、视频。')
    media_credit = models.CharField(u'媒体版权', max_length=255, blank=True, null=True, help_text=u'')
    media_caption = models.TextField(u'媒体说明', blank=True, null=True, help_text=u'')

    cover = models.BooleanField(u'封面', help_text=u"", default=False)

    def __unicode__(self):
        return "%s-%s" % (self.timeline.title, self.title)

class Comment(models.Model):
    timeline = models.ForeignKey(Timeline)
    content = models.TextField()

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(u'创建日期', auto_now_add=True)

    def __unicode__(self):
        return "%s-%s" % (self.timeline.title, self.content[:20])

"""
class Apply(models.Model):
    STATUS_CHOICES = (('todo', u'待批复'), 
            ('rejected', u'驳回'),
            ('approved', u'批准'))
    timeline = models.ForeignKey(Timeline)
    applicant = models.ForeignKey(User)
    reply_on = models.DateTimeField(u'批复时间', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(u"状态", max_length=16, default='draft', choices=STATUS_CHOICES)
"""
