# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Product.description'
        db.alter_column('catalog_product', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Manufacturer.image'
        db.alter_column('catalog_manufacturer', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'Manufacturer.description'
        db.alter_column('catalog_manufacturer', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Category.description'
        db.alter_column('catalog_category', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Category.image'
        db.alter_column('catalog_category', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

    def backwards(self, orm):

        # Changing field 'Product.description'
        db.alter_column('catalog_product', 'description', self.gf('django.db.models.fields.TextField')(default=''))

        # User chose to not deal with backwards NULL issues for 'Manufacturer.image'
        raise RuntimeError("Cannot reverse this migration. 'Manufacturer.image' and its values cannot be restored.")

        # Changing field 'Manufacturer.description'
        db.alter_column('catalog_manufacturer', 'description', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Category.description'
        db.alter_column('catalog_category', 'description', self.gf('django.db.models.fields.TextField')(default=''))

        # User chose to not deal with backwards NULL issues for 'Category.image'
        raise RuntimeError("Cannot reverse this migration. 'Category.image' and its values cannot be restored.")

    models = {
        'catalog.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['catalog.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'catalog.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127'})
        },
        'catalog.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Manufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '13'})
        },
        'catalog.productattribute': {
            'Meta': {'object_name': 'ProductAttribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attribute'", 'to': "orm['catalog.Product']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'catalog.productimages': {
            'Meta': {'object_name': 'ProductImages'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['catalog.Product']"})
        }
    }

    complete_apps = ['catalog']