# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table('user_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('nick_name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('cell_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('home_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('work_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('emergency_first_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('emergency_last_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('emergency_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('user', ['Profile'])

        # Adding model 'CrossName'
        db.create_table('user_crossname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('user', ['CrossName'])

        # Adding model 'CrossReference'
        db.create_table('user_crossreference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.CrossName'])),
            ('reference', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.Profile'])),
        ))
        db.send_create_signal('user', ['CrossReference'])

        # Adding unique constraint on 'CrossReference', fields ['name', 'profile']
        db.create_unique('user_crossreference', ['name_id', 'profile_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'CrossReference', fields ['name', 'profile']
        db.delete_unique('user_crossreference', ['name_id', 'profile_id'])

        # Deleting model 'Profile'
        db.delete_table('user_profile')

        # Deleting model 'CrossName'
        db.delete_table('user_crossname')

        # Deleting model 'CrossReference'
        db.delete_table('user_crossreference')


    models = {
        'user.crossname': {
            'Meta': {'object_name': 'CrossName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'user.crossreference': {
            'Meta': {'unique_together': "(('name', 'profile'),)", 'object_name': 'CrossReference'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user.CrossName']"}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user.Profile']"}),
            'reference': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'user.profile': {
            'Meta': {'object_name': 'Profile'},
            'cell_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'emergency_first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'emergency_last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'emergency_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'nick_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'work_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['user']