# -*- coding: UTF-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

from timeline.models import Timeline

class ViewsBaseCase(TestCase):

    fixtures = ['test_timeline_users.json', 
            'test_timeline_timelines.json']

class ViewsSimpleTest(ViewsBaseCase):

    def test_idx(self):
        resp = self.client.get(reverse('timeline_idx'))
        self.assertEqual(resp.status_code, 200)

    def test_hot(self):
        resp = self.client.get(reverse('timeline_hot'))
        self.assertEqual(resp.status_code, 200)

    def test_recommend(self):
        resp = self.client.get(reverse('timeline_recommend'))
        self.assertEqual(resp.status_code, 200)

    def test_last(self):
        resp = self.client.get(reverse('timeline_last'))
        self.assertEqual(resp.status_code, 200)

    def test_random(self):
        resp = self.client.get(reverse('timeline_random'))
        self.assertEqual(resp.status_code, 200)

    def test_tags(self):
        resp = self.client.get(reverse('timeline_tags'))
        self.assertEqual(resp.status_code, 200)

    def test_full_screen(self):
        resp = self.client.get(reverse('timeline_full_screen', args=(1, )))
        self.assertEqual(resp.status_code, 200)

    def test_detail(self):
        resp = self.client.get(reverse('timeline_detail', args=(1, )))
        self.assertEqual(resp.status_code, 200)

    def test_events(self):
        resp = self.client.get(reverse('timeline_events', args=(1, )))
        self.assertEqual(resp.status_code, 200)

        assert self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('timeline_events', args=(1, )))
        self.assertEqual(resp.status_code, 200)

    def test_events_json_(self):
        resp = self.client.get(reverse('timeline_events_json_', args=(1, )))
        self.assertEqual(resp.status_code, 200)

    def test_events_sjson_(self):
        resp = self.client.get(reverse('timeline_events_sjson_', args=(1, )))
        self.assertEqual(resp.status_code, 200)

class DeleteTimelineTest(ViewsBaseCase):

    def test_delete(self):
        resp = self.client.post(reverse('timeline_delete', args=[1]))
        self.assertEqual(resp.status_code, 302)

        assert self.client.login(username='user', password='user')
        resp = self.client.post(reverse('timeline_delete', args=[1]))
        self.assertEqual(resp.status_code, 200)
        assert len(resp.content) < 100

        assert self.client.login(username='admin', password='admin')
        resp = self.client.post(reverse('timeline_delete', args=[1]))
        self.assertEqual(resp.status_code, 302)
        tl = Timeline.objects.get(pk=1)
        self.assertEqual(tl.status, 'del')

class NewTimelineTest(ViewsBaseCase):

    def test_new(self):
        #not login
        resp = self.client.post(reverse('timeline_new'))
        self.assertEqual(resp.status_code, 302)
        #login
        assert self.client.login(username='user', password='user')
        #no param
        resp = self.client.post(reverse('timeline_new'))
        self.assertEqual(resp.status_code, 200)
        #ok
        resp = self.client.post(reverse('timeline_new'), 
                {'status': 'draft', 
                    'title': 'new timeline', 
                    'tags': 'test,some', 
                    'intro': 'intro...'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Timeline.objects.filter(title='new timeline').count(), 1)
