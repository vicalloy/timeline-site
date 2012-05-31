# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Timeline'
        db.create_table('timeline_timeline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('intro', self.gf('django.db.models.fields.TextField')(max_length=30)),
            ('focus_date', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('status', self.gf('django.db.models.fields.CharField')(default='draft', max_length=16)),
            ('num_events', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_replies', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('rec', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rec_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('timeline', ['Timeline'])

        # Adding M2M table for field attachments on 'Timeline'
        db.create_table('timeline_timeline_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('timeline', models.ForeignKey(orm['timeline.timeline'], null=False)),
            ('attachment', models.ForeignKey(orm['attachments.attachment'], null=False))
        ))
        db.create_unique('timeline_timeline_attachments', ['timeline_id', 'attachment_id'])

        # Adding model 'TlEvent'
        db.create_table('timeline_tlevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timeline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timeline.Timeline'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('startdate', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('enddate', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('media', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('media_credit', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('media_caption', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cover', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('timeline', ['TlEvent'])

        # Adding model 'Comment'
        db.create_table('timeline_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timeline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timeline.Timeline'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('timeline', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Timeline'
        db.delete_table('timeline_timeline')

        # Removing M2M table for field attachments on 'Timeline'
        db.delete_table('timeline_timeline_attachments')

        # Deleting model 'TlEvent'
        db.delete_table('timeline_tlevent')

        # Deleting model 'Comment'
        db.delete_table('timeline_comment')


    models = {
        'attachments.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_img': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num_downloads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'org_filename': ('django.db.models.fields.TextField', [], {}),
            'suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        },
        'timeline.comment': {
            'Meta': {'object_name': 'Comment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['timeline.Timeline']"})
        },
        'timeline.timeline': {
            'Meta': {'object_name': 'Timeline'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attachments.Attachment']", 'symmetrical': 'False', 'blank': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'focus_date': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'max_length': '30'}),
            'num_events': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_replies': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'num_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rec': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rec_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '16'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        'timeline.tlevent': {
            'Meta': {'object_name': 'TlEvent'},
            'cover': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enddate': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'media_caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'media_credit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['timeline.Timeline']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['timeline']