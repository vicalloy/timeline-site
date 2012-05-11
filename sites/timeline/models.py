# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User

from easy_thumbnails.fields import ThumbnailerImageField
from taggit.managers import TaggableManager

def upload_to_cover(instance, filename):
    extension = filename.split('.')[-1].lower()
    return '%(path)s%(pk)s.%(extension)s' % {'path': 'cover/',
                                               'pk': instance.pk,
                                               'extension': extension}

class Timeline(models.Model):
    title = models.CharField(u'标题', max_length=30)
    cover = ThumbnailerImageField(u'封面',
            blank=True,
            upload_to=upload_to_cover,
            resize_source={'size': (140,140), 'crop': 'smart'},
            help_text=u'封面图片')
    tags = TaggableManager(blank=True)
    intro = models.TextField(u'简介', max_length=30)
    focus_date = models.CharField(u'初始日期', max_length=30)

    num_events = models.IntegerField(u'事件数', default=0)
    num_views = models.IntegerField(u'浏览次数', default=0)
    num_replies = models.PositiveSmallIntegerField(u'回复数', default=0)#posts...
    #TODO status draft...
    #TODO TAGS...
    #rec 推荐

    rec = models.BooleanField(u'推荐', default=False)
    rec_on = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return self.title

class TlEvent(models.Model):
    timeline = models.ForeignKey(Timeline)
    title = models.CharField(u'标题', max_length=30)
    startdate = models.DateTimeField(u'开始日期', help_text=u"日期格式")
    enddate = models.DateTimeField(u'结束日期', blank=True, null=True, help_text=u"日期格式")
    text = models.TextField(u'详细说明', blank=True, null=True, help_text=u'详细说明')

    media = models.TextField(u'媒体', max_length=255, blank=True, null=True, help_text=u'媒体文件，可以是图片地址。')
    media_credit = models.CharField(u'媒体版权', max_length=255, blank=True, null=True, help_text=u'')
    media_caption = models.CharField(u'媒体标题', max_length=255, blank=True, null=True, help_text=u'')

    cover = models.BooleanField(u'封面', help_text=u"", default=False)

    def __unicode__(self):
        return "%s-%s" % (self.timeline.title, self.title)
