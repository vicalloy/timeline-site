# -*- coding: UTF-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

from timeline.models import Timeline

class ViewsBaseCase(TestCase):

    fixtures = ['test_timeline_users.json', 
            'test_timeline_timelines.json']

    def setUp(self):
        timeline = Timeline.objects.get(pk=1)
        timeline.tags.add('test', 'tag')

class BaseViewsTest(ViewsBaseCase):

    def setUp(self):
        super(BaseViewsTest, self).setUp()
        #assert self.client.login(username='user', password='user')

    def test_idx(self):
        resp = self.client.get(reverse('timeline_idx'))
        self.assertEquals(resp.status_code, 200)

    def test_hot(self):
        resp = self.client.get(reverse('timeline_hot'))
        self.assertEquals(resp.status_code, 200)

    def test_recommend(self):
        resp = self.client.get(reverse('timeline_recommend'))
        self.assertEquals(resp.status_code, 200)

    def test_last(self):
        resp = self.client.get(reverse('timeline_last'))
        self.assertEquals(resp.status_code, 200)

    def test_random(self):
        resp = self.client.get(reverse('timeline_random'))
        self.assertEquals(resp.status_code, 200)

    def test_tags(self):
        resp = self.client.get(reverse('timeline_tags'))
        self.assertEquals(resp.status_code, 200)

    def test_full_screen(self):
        resp = self.client.get(reverse('timeline_full_screen', args=(1, )))
        self.assertEquals(resp.status_code, 200)

    def test_detail(self):
        resp = self.client.get(reverse('timeline_detail', args=(1, )))
        self.assertEquals(resp.status_code, 200)
