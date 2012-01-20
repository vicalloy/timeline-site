# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Timeline(models.Model):
    title = models.CharField(u'标题', max_length=30)
    intro = models.CharField(u'简介', max_length=30)
    num_events = models.IntegerField(u'事件数', default = 0)
    num_views = models.IntegerField(u'浏览次数', default=0)
    num_replies = models.PositiveSmallIntegerField(u'回复数', default=0)#posts...
    #TODO status draft...
    #TODO TAGS...

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(blank = True, null = True)
    
    def __unicode__(self):
        return self.title

class Recommend(models.Model):
    timeline = models.ForeignKey(Timeline)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(blank = True, null = True)

    def __unicode__(self):
        return self.timeline.title
