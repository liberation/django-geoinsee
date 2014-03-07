# -*- coding: utf-8 -*-
import os
import json
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def update_zipcode(self, orm, item):
        locality = orm.Locality.objects.get(code=item['code'])
        locality.zipcode = item['zipcode']
        if not db.dry_run:
            locality.save()

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        data_file_path = os.path.realpath(
                        os.path.join(
                            os.path.dirname(__file__),
                            'data',
                            '0005_zipcodes.json'
                        )
                    )
        # read file and load JSON data
        f = open(data_file_path, 'r')
        content = f.read()
        data = json.loads(content)
        for item in data:
            self.update_zipcode(orm, item)

    def backwards(self, orm):
        "Write your backwards methods here."
        data_file_path = os.path.realpath(
                        os.path.join(
                            os.path.dirname(__file__),
                            'data',
                            '0005_zipcodes_backwards.json'
                        )
                    )
        # read file and load JSON data
        f = open(data_file_path, 'r')
        content = f.read()
        data = json.loads(content)
        for item in data:
            self.update_zipcode(orm, item)

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
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geoinsee.Locality']", 'null': 'True'}),
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
    symmetrical = True
