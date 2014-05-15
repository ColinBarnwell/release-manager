# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Environment'
        db.create_table(u'relman_environment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relman.Package'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('promotes_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relman.Environment'], null=True, blank=True)),
        ))
        db.send_create_signal('relman', ['Environment'])

        # Adding unique constraint on 'Environment', fields ['package', 'name']
        db.create_unique(u'relman_environment', ['package_id', 'name'])

        # Adding model 'Promotion'
        db.create_table(u'relman_promotion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('environment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relman.Environment'])),
            ('build', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relman.Build'])),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('relman', ['Promotion'])

        # Adding model 'Package'
        db.create_table(u'relman_package', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('relman', ['Package'])

        # Adding model 'PackageVersion'
        db.create_table(u'relman_packageversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('major_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('minor_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('patch_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('alpha_version', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('target_date', self.gf('django.db.models.fields.DateField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relman.Package'])),
            ('previous_version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relman.PackageVersion'], null=True, blank=True)),
        ))
        db.send_create_signal('relman', ['PackageVersion'])

        # Adding model 'Product'
        db.create_table(u'relman_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('relman', ['Product'])

        # Adding model 'ProductRelease'
        db.create_table(u'relman_productrelease', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('major_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('minor_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('patch_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('alpha_version', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('target_date', self.gf('django.db.models.fields.DateField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relman.Product'])),
            ('previous_release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relman.ProductRelease'], null=True, blank=True)),
        ))
        db.send_create_signal('relman', ['ProductRelease'])

        # Adding M2M table for field dependencies on 'ProductRelease'
        m2m_table_name = db.shorten_name(u'relman_productrelease_dependencies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('productrelease', models.ForeignKey(orm['relman.productrelease'], null=False)),
            ('packageversion', models.ForeignKey(orm['relman.packageversion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['productrelease_id', 'packageversion_id'])

        # Adding model 'Build'
        db.create_table(u'relman_build', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relman.ProductRelease'])),
            ('build_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('code_name', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('relman', ['Build'])


    def backwards(self, orm):
        # Removing unique constraint on 'Environment', fields ['package', 'name']
        db.delete_unique(u'relman_environment', ['package_id', 'name'])

        # Deleting model 'Environment'
        db.delete_table(u'relman_environment')

        # Deleting model 'Promotion'
        db.delete_table(u'relman_promotion')

        # Deleting model 'Package'
        db.delete_table(u'relman_package')

        # Deleting model 'PackageVersion'
        db.delete_table(u'relman_packageversion')

        # Deleting model 'Product'
        db.delete_table(u'relman_product')

        # Deleting model 'ProductRelease'
        db.delete_table(u'relman_productrelease')

        # Removing M2M table for field dependencies on 'ProductRelease'
        db.delete_table(db.shorten_name(u'relman_productrelease_dependencies'))

        # Deleting model 'Build'
        db.delete_table(u'relman_build')


    models = {
        'relman.build': {
            'Meta': {'object_name': 'Build'},
            'build_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.ProductRelease']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'relman.environment': {
            'Meta': {'unique_together': "(('package', 'name'),)", 'object_name': 'Environment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.Package']"}),
            'promotes_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.Environment']", 'null': 'True', 'blank': 'True'})
        },
        'relman.package': {
            'Meta': {'object_name': 'Package'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'relman.packageversion': {
            'Meta': {'ordering': "('major_version', 'minor_version', 'patch_version', 'alpha_version')", 'object_name': 'PackageVersion'},
            'alpha_version': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'minor_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.Package']"}),
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
            'Meta': {'ordering': "('major_version', 'minor_version', 'patch_version', 'alpha_version')", 'object_name': 'ProductRelease'},
            'alpha_version': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'depended_by'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['relman.PackageVersion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'minor_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'patch_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'previous_release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.ProductRelease']", 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.Product']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'target_date': ('django.db.models.fields.DateField', [], {})
        },
        'relman.promotion': {
            'Meta': {'object_name': 'Promotion'},
            'build': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.Build']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.Environment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['relman']