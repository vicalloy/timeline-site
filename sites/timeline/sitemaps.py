# -*- coding: UTF-8 -*-
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from timeline.models import get_all_timlines

class TimelineSitemap(Sitemap):
    def items(self):
        return get_all_timlines()

    def lastmod(self, obj):
        return obj.updated_on

class TimelineEventsSitemap(Sitemap):
    def items(self):
        return get_all_timlines()

    def lastmod(self, obj):
        return obj.updated_on

    def location(self, obj):
        return reverse('timeline_events', args=[obj.pk])

sitemaps = {
    'timeline': TimelineSitemap,
    'timelineevents': TimelineEventsSitemap,
}
