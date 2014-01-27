# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'State'
        db.create_table(u'geoinsee_state', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='state_admin', null=True, to=orm['geoinsee.Locality'])),
        ))
        db.send_create_signal(u'geoinsee', ['State'])

        # Adding model 'Division'
        db.create_table(u'geoinsee_division', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='division_state', to=orm['geoinsee.State'])),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='division_admin', to=orm['geoinsee.Locality'])),
        ))
        db.send_create_signal(u'geoinsee', ['Division'])

        # Adding model 'District'
        db.create_table(u'geoinsee_district', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=8, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='district_state', to=orm['geoinsee.State'])),
            ('division', self.gf('django.db.models.fields.related.ForeignKey')(related_name='district_division', to=orm['geoinsee.Division'])),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='district_admin', to=orm['geoinsee.Locality'])),
        ))
        db.send_create_signal(u'geoinsee', ['District'])

        # Adding model 'County'
        db.create_table(u'geoinsee_county', (
            ('code', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('typology', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
        ))
        db.send_create_signal(u'geoinsee', ['County'])

        # Adding model 'Locality'
        db.create_table(u'geoinsee_locality', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, db_index=True)),
            ('typology', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('surface', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('population', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=9)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=9)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoinsee.State'], null=True)),
            ('division', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoinsee.Division'], null=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoinsee.District'], null=True)),
            ('county', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoinsee.County'], null=True)),
            ('employmentzone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geoinsee.EmploymentZone'], null=True)),
        ))
        db.send_create_signal(u'geoinsee', ['Locality'])

        # Adding model 'EmploymentZone'
        db.create_table(u'geoinsee_employmentzone', (
            ('code', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
        ))
        db.send_create_signal(u'geoinsee', ['EmploymentZone'])


    def backwards(self, orm):
        # Deleting model 'State'
        db.delete_table(u'geoinsee_state')

        # Deleting model 'Division'
        db.delete_table(u'geoinsee_division')

        # Deleting model 'District'
        db.delete_table(u'geoinsee_district')

        # Deleting model 'County'
        db.delete_table(u'geoinsee_county')

        # Deleting model 'Locality'
        db.delete_table(u'geoinsee_locality')

        # Deleting model 'EmploymentZone'
        db.delete_table(u'geoinsee_employmentzone')


    models = {
        u'geoinsee.county': {
            'Meta': {'object_name': 'County'},
            'code': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'typology': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'})
        },
        u'geoinsee.district': {
            'Meta': {'object_name': 'District'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'district_admin'", 'to': u"orm['geoinsee.Locality']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'district_division'", 'to': u"orm['geoinsee.Division']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'district_state'", 'to': u"orm['geoinsee.State']"})
        },
        u'geoinsee.division': {
            'Meta': {'object_name': 'Division'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'division_admin'", 'to': u"orm['geoinsee.Locality']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'division_state'", 'to': u"orm['geoinsee.State']"})
        },
        u'geoinsee.employmentzone': {
            'Meta': {'object_name': 'EmploymentZone'},
            'code': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        },
        u'geoinsee.locality': {
            'Meta': {'object_name': 'Locality'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'county': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoinsee.County']", 'null': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoinsee.District']", 'null': 'True'}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoinsee.Division']", 'null': 'True'}),
            'employmentzone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoinsee.EmploymentZone']", 'null': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '9'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '9'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'population': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoinsee.State']", 'null': 'True'}),
            'surface': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'typology': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'db_index': 'True'})
        },
        u'geoinsee.state': {
            'Meta': {'object_name': 'State'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'state_admin'", 'null': 'True', 'to': u"orm['geoinsee.Locality']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['geoinsee']