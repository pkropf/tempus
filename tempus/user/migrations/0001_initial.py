# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HistoricalProfile'
        db.create_table('user_historicalprofile', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
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
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('user', ['HistoricalProfile'])

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

        # Adding model 'HistoricalCrossName'
        db.create_table('user_historicalcrossname', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('user', ['HistoricalCrossName'])

        # Adding model 'CrossName'
        db.create_table('user_crossname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('user', ['CrossName'])

        # Adding model 'HistoricalCrossReference'
        db.create_table('user_historicalcrossreference', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('profile', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('user', ['HistoricalCrossReference'])

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

        # Deleting model 'HistoricalProfile'
        db.delete_table('user_historicalprofile')

        # Deleting model 'Profile'
        db.delete_table('user_profile')

        # Deleting model 'HistoricalCrossName'
        db.delete_table('user_historicalcrossname')

        # Deleting model 'CrossName'
        db.delete_table('user_crossname')

        # Deleting model 'HistoricalCrossReference'
        db.delete_table('user_historicalcrossreference')

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
        'user.historicalcrossname': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalCrossName'},
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'user.historicalcrossreference': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalCrossReference'},
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'user.historicalprofile': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalProfile'},
            'cell_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'emergency_first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'emergency_last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'emergency_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'nick_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'work_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
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