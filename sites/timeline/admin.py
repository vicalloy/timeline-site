# -*- coding: UTF-8 -*-
from django.contrib import admin

from timeline.models import Timeline, TlEvent, Comment

class TimelineAdmin(admin.ModelAdmin):
    list_display        = ('title', 'rec', 'created_by', 'status', 'num_events', 'num_views', 'num_replies', )
    search_fields       = ('title', 'created_by__username', )
    raw_id_fields       = ('attachments', 'created_by')
    #list_filter         = ('category',)
admin.site.register(Timeline, TimelineAdmin)

class TlEventAdmin(admin.ModelAdmin):
    list_display        = ('timeline', 'title', 'startdate', 'cover', )
    search_fields       = ('title', 'timeline__title', )
    raw_id_fields       = ("timeline", )
admin.site.register(TlEvent, TlEventAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display        = ('timeline', 'created_by', 'content', )
    search_fields       = ('timeline__title', 'content', 'created_by__username', )
    raw_id_fields       = ('timeline', 'created_by', )
admin.site.register(Comment, CommentAdmin)
