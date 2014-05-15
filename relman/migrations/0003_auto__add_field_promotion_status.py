# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Promotion.status'
        db.add_column(u'relman_promotion', 'status',
                      self.gf('django.db.models.fields.CharField')(default='awaiting', max_length=16),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Promotion.status'
        db.delete_column(u'relman_promotion', 'status')


    models = {
        'relman.build': {
            'Meta': {'ordering': "('build_number',)", 'unique_together': "(('release', 'build_number'),)", 'object_name': 'Build'},
            'build_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'builds'", 'to': "orm['relman.ProductRelease']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'relman.environment': {
            'Meta': {'unique_together': "(('product', 'name'),)", 'object_name': 'Environment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.Product']"}),
            'promotes_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.Environment']", 'null': 'True', 'blank': 'True'})
        },
        'relman.package': {
            'Meta': {'object_name': 'Package'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'relman.packageversion': {
            'Meta': {'ordering': "('-major_version', '-minor_version', '-patch_version', 'alpha_version')", 'object_name': 'PackageVersion'},
            'alpha_version': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'minor_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['relman.Package']"}),
            'patch_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'previous_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.PackageVersion']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'target_date': ('django.db.models.fields.DateField', [], {})
        },
        'relman.product': {
            'Meta': {'object_name': 'Product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'relman.productrelease': {
            'Meta': {'ordering': "('-major_version', '-minor_version', '-patch_version', 'alpha_version')", 'object_name': 'ProductRelease'},
            'alpha_version': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'depended_by'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['relman.PackageVersion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'minor_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'patch_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'previous_release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.ProductRelease']", 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['relman.Product']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'target_date': ('django.db.models.fields.DateField', [], {})
        },
        'relman.promotion': {
            'Meta': {'object_name': 'Promotion'},
            'build': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'promotions'", 'to': "orm['relman.Build']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.Environment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'awaiting'", 'max_length': '16'})
        }
    }

    complete_apps = ['relman']