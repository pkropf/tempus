# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rfidcard'
        db.create_table('timecard_rfidcard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rfid', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.Profile'], null=True, blank=True)),
        ))
        db.send_create_signal('timecard', ['Rfidcard'])

        # Adding model 'TimecardType'
        db.create_table('timecard_timecardtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('ranking', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('timecard', ['TimecardType'])

        # Adding model 'Timecard'
        db.create_table('timecard_timecard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timecardtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timecard.TimecardType'])),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.Profile'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('timecard', ['Timecard'])

        # Adding model 'Stamp'
        db.create_table('timecard_stamp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('timecard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timecard.Timecard'])),
        ))
        db.send_create_signal('timecard', ['Stamp'])


    def backwards(self, orm):
        # Deleting model 'Rfidcard'
        db.delete_table('timecard_rfidcard')

        # Deleting model 'TimecardType'
        db.delete_table('timecard_timecardtype')

        # Deleting model 'Timecard'
        db.delete_table('timecard_timecard')

        # Deleting model 'Stamp'
        db.delete_table('timecard_stamp')


    models = {
        'timecard.rfidcard': {
            'Meta': {'object_name': 'Rfidcard'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user.Profile']", 'null': 'True', 'blank': 'True'}),
            'rfid': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        },
        'timecard.stamp': {
            'Meta': {'object_name': 'Stamp'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'timecard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['timecard.Timecard']"})
        },
        'timecard.timecard': {
            'Meta': {'ordering': "['profile', 'start_date']", 'object_name': 'Timecard'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user.Profile']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'timecardtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['timecard.TimecardType']"})
        },
        'timecard.timecardtype': {
            'Meta': {'object_name': 'TimecardType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ranking': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
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

    complete_apps = ['timecard']