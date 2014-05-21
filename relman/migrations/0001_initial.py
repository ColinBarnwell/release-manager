# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Checkpoint'
        db.create_table(u'relman_checkpoint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('relman', ['Checkpoint'])

        # Adding model 'Check'
        db.create_table(u'relman_check', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('build', self.gf('django.db.models.fields.related.ForeignKey')(related_name='checks', to=orm['relman.Build'])),
            ('checkpoint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relman.Checkpoint'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='awaiting', max_length=16)),
        ))
        db.send_create_signal('relman', ['Check'])

        # Adding unique constraint on 'Check', fields ['build', 'checkpoint']
        db.create_unique(u'relman_check', ['build_id', 'checkpoint_id'])

        # Adding model 'Package'
        db.create_table(u'relman_package', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('relman', ['Package'])

        # Adding model 'PackageVersion'
        db.create_table(u'relman_packageversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='proposed', max_length=16)),
            ('major_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('minor_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('patch_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('target_date', self.gf('django.db.models.fields.DateField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='versions', to=orm['relman.Package'])),
        ))
        db.send_create_signal('relman', ['PackageVersion'])

        # Adding model 'PackageVersionBuild'
        db.create_table(u'relman_packageversionbuild', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='builds', to=orm['relman.PackageVersion'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('relman', ['PackageVersionBuild'])

        # Adding unique constraint on 'PackageVersionBuild', fields ['version', 'code']
        db.create_unique(u'relman_packageversionbuild', ['version_id', 'code'])

        # Adding model 'Change'
        db.create_table(u'relman_change', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changes', to=orm['relman.PackageVersion'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('relman', ['Change'])

        # Adding model 'Product'
        db.create_table(u'relman_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('relman', ['Product'])

        # Adding model 'ProductRelease'
        db.create_table(u'relman_productrelease', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='proposed', max_length=16)),
            ('major_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('minor_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('patch_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('target_date', self.gf('django.db.models.fields.DateField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='releases', to=orm['relman.Product'])),
            ('release_manager', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
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
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='builds', to=orm['relman.ProductRelease'])),
            ('build_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('code_name', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('relman', ['Build'])

        # Adding unique constraint on 'Build', fields ['release', 'build_number']
        db.create_unique(u'relman_build', ['release_id', 'build_number'])

        # Adding model 'Comment'
        db.create_table(u'relman_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('relman', ['Comment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Build', fields ['release', 'build_number']
        db.delete_unique(u'relman_build', ['release_id', 'build_number'])

        # Removing unique constraint on 'PackageVersionBuild', fields ['version', 'code']
        db.delete_unique(u'relman_packageversionbuild', ['version_id', 'code'])

        # Removing unique constraint on 'Check', fields ['build', 'checkpoint']
        db.delete_unique(u'relman_check', ['build_id', 'checkpoint_id'])

        # Deleting model 'Checkpoint'
        db.delete_table(u'relman_checkpoint')

        # Deleting model 'Check'
        db.delete_table(u'relman_check')

        # Deleting model 'Package'
        db.delete_table(u'relman_package')

        # Deleting model 'PackageVersion'
        db.delete_table(u'relman_packageversion')

        # Deleting model 'PackageVersionBuild'
        db.delete_table(u'relman_packageversionbuild')

        # Deleting model 'Change'
        db.delete_table(u'relman_change')

        # Deleting model 'Product'
        db.delete_table(u'relman_product')

        # Deleting model 'ProductRelease'
        db.delete_table(u'relman_productrelease')

        # Removing M2M table for field dependencies on 'ProductRelease'
        db.delete_table(db.shorten_name(u'relman_productrelease_dependencies'))

        # Deleting model 'Build'
        db.delete_table(u'relman_build')

        # Deleting model 'Comment'
        db.delete_table(u'relman_comment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'relman.build': {
            'Meta': {'ordering': "('build_number',)", 'unique_together': "(('release', 'build_number'),)", 'object_name': 'Build'},
            'build_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'builds'", 'to': "orm['relman.ProductRelease']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'relman.change': {
            'Meta': {'object_name': 'Change'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changes'", 'to': "orm['relman.PackageVersion']"})
        },
        'relman.check': {
            'Meta': {'unique_together': "(('build', 'checkpoint'),)", 'object_name': 'Check'},
            'build': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checks'", 'to': "orm['relman.Build']"}),
            'checkpoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relman.Checkpoint']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'awaiting'", 'max_length': '16'})
        },
        'relman.checkpoint': {
            'Meta': {'ordering': "('display_order', 'name')", 'object_name': 'Checkpoint'},
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'relman.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'relman.package': {
            'Meta': {'object_name': 'Package'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'relman.packageversion': {
            'Meta': {'ordering': "('-major_version', '-minor_version', '-patch_version')", 'object_name': 'PackageVersion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'minor_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['relman.Package']"}),
            'patch_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'proposed'", 'max_length': '16'}),
            'target_date': ('django.db.models.fields.DateField', [], {})
        },
        'relman.packageversionbuild': {
            'Meta': {'ordering': "('-code',)", 'unique_together': "(('version', 'code'),)", 'object_name': 'PackageVersionBuild'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'builds'", 'to': "orm['relman.PackageVersion']"})
        },
        'relman.product': {
            'Meta': {'object_name': 'Product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'relman.productrelease': {
            'Meta': {'ordering': "('-major_version', '-minor_version', '-patch_version')", 'object_name': 'ProductRelease'},
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'dependants'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['relman.PackageVersion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'minor_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'patch_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['relman.Product']"}),
            'release_manager': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'proposed'", 'max_length': '16'}),
            'target_date': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['relman']