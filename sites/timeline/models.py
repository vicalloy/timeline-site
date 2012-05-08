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
    timezone = models.CharField(u'时区', max_length=30)
    initial_zoom = models.CharField(u'初始缩放大小', max_length=30)
    num_events = models.IntegerField(u'事件数', default=0)
    num_views = models.IntegerField(u'浏览次数', default=0)
    num_replies = models.PositiveSmallIntegerField(u'回复数', default=0)#posts...
    #TODO status draft...
    #TODO TAGS...
    #rec 推荐

    rec = models.BooleanField(u'推荐', default=False)
    rec_on = models.DateTimeField(blank = True, null = True)

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(blank = True, null = True)
    
    def __unicode__(self):
        return self.title

class TlEvent(models.Model):
    timeline = models.ForeignKey(Timeline)
    title = models.CharField(u'标题', max_length=30)
    #TODO 小图片说明
    description = models.CharField(u'描述', max_length=3000)
    startdate = models.CharField(u'开始日期', max_length=30)
    enddate = models.CharField(u'结束日期', max_length=30)
    date_display = models.CharField(u'日期格式', max_length=30)#TODO MOVE TO TIMELINE...
    link = models.CharField(u'链接', max_length=30)
    icon = models.CharField(u'图标', max_length=30)
    importance = models.CharField(u'权重', max_length=30)
    #some attachments?
