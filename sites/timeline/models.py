# -*- coding: UTF-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from attachments.models import Attachment
from easy_thumbnails.fields import ThumbnailerImageField
from taggit.managers import TaggableManager

def upload_to_cover(instance, filename):
    extension = filename.split('.')[-1].lower()
    return '%(path)s%(pk)s.%(extension)s' % {'path': 'cover/',
                                               'pk': instance.pk,
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
    intro = models.TextField(u'简介', max_length=30)
    focus_date = models.CharField(u'初始日期', max_length=30)
    attachments = models.ManyToManyField(Attachment, blank = True)
    status = models.CharField(u"发布状态", max_length=16, default='draft', choices=STATUS_CHOICES)

    num_events = models.IntegerField(u'事件数', default=0)
    num_views = models.IntegerField(u'浏览次数', default=0)
    num_replies = models.PositiveSmallIntegerField(u'回复数', default=0)#posts...

    rec = models.BooleanField(u'推荐', default=False)
    rec_on = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __unicode__(self):
        return self.title

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

class TlEvent(models.Model):
    timeline = models.ForeignKey(Timeline)
    title = models.CharField(u'标题', max_length=30)
    startdate = models.CharField(u'开始日期', max_length=32, help_text=u"支持的日期格式：, yyyy-mm-dd(2012-12-20)、yyyy(2012)")
    enddate = models.CharField(u'结束日期', max_length=32, blank=True, null=True, help_text=u"支持的日期格式：, yyyy-mm-dd(2012-12-20)、yyyy(2012)")
    text = models.TextField(u'详细说明', blank=True, null=True, help_text=u'详细说明')

    media = models.TextField(u'媒体', blank=True, null=True, help_text=u'媒体文件，可以是图片地址。')
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
