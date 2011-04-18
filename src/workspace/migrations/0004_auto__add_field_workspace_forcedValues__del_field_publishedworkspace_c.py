# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'WorkSpace.forcedValues'
        db.add_column('workspace_workspace', 'forcedValues', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Deleting field 'PublishedWorkSpace.credentials'
        db.delete_column('workspace_publishedworkspace', 'credentials')

        # Deleting field 'PublishedWorkSpace.type'
        db.delete_column('workspace_publishedworkspace', 'type')

        # Adding field 'PublishedWorkSpace.creator'
        db.add_column('workspace_publishedworkspace', 'creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True), keep_default=False)

        # Adding field 'PublishedWorkSpace.template'
        db.add_column('workspace_publishedworkspace', 'template', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'PublishedWorkSpace.params'
        db.add_column('workspace_publishedworkspace', 'params', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Changing field 'PublishedWorkSpace.workspace'
        db.alter_column('workspace_publishedworkspace', 'workspace_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workspace.WorkSpace'], null=True))

    def backwards(self, orm):

        # Deleting field 'WorkSpace.forcedValues'
        db.delete_column('workspace_workspace', 'forcedValues')

        # Adding field 'PublishedWorkSpace.credentials'
        db.add_column('workspace_publishedworkspace', 'credentials', self.gf('django.db.models.fields.CharField')(default='', max_length=30), keep_default=False)

        # Adding field 'PublishedWorkSpace.type'
        db.add_column('workspace_publishedworkspace', 'type', self.gf('django.db.models.fields.CharField')(default='CLONED', max_length=10), keep_default=False)

        # Deleting field 'PublishedWorkSpace.creator'
        db.delete_column('workspace_publishedworkspace', 'creator_id')

        # Deleting field 'PublishedWorkSpace.template'
        db.delete_column('workspace_publishedworkspace', 'template')

        # Deleting field 'PublishedWorkSpace.params'
        db.delete_column('workspace_publishedworkspace', 'params')

        # User chose to not deal with backwards NULL issues for 'PublishedWorkSpace.workspace'
        raise RuntimeError("Cannot reverse this migration. 'PublishedWorkSpace.workspace' and its values cannot be restored.")

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
        },
        'gadget.sharedvariabledef': {
            'Meta': {'object_name': 'SharedVariableDef'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
        },
        'workspace.abstractvariable': {
            'Meta': {'object_name': 'AbstractVariable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
        },
        'workspace.category': {
            'Meta': {'object_name': 'Category'},
            'category_id': ('django.db.models.fields.IntegerField', [], {}),
            'default_workspace': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workspace.PublishedWorkSpace']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_workspace': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'new_workspace_'", 'null': 'True', 'to': "orm['workspace.PublishedWorkSpace']"}),
        },
        'workspace.publishedworkspace': {
            'Meta': {'object_name': 'PublishedWorkSpace'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'contratable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageURI': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'mail': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {}),
            'template': ('django.db.models.fields.TextField', [], {}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'wikiURI': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'workspace': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workspace.WorkSpace']", 'null': 'True', 'blank': 'True'}),
        },
        'workspace.sharedvariablevalue': {
            'Meta': {'unique_together': "(('shared_var_def', 'user'),)", 'object_name': 'SharedVariableValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shared_var_def': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gadget.SharedVariableDef']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
        },
        'workspace.tab': {
            'Meta': {'object_name': 'Tab'},
            'abstract_variable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workspace.AbstractVariable']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'workspace': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workspace.WorkSpace']"}),
        },
        'workspace.userworkspace': {
            'Meta': {'object_name': 'UserWorkSpace'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'workspace': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workspace.WorkSpace']"}),
        },
        'workspace.variablevalue': {
            'Meta': {'object_name': 'VariableValue'},
            'abstract_variable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workspace.AbstractVariable']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shared_var_value': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workspace.SharedVariableValue']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
        },
        'workspace.workspace': {
            'Meta': {'object_name': 'WorkSpace'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator'", 'to': "orm['auth.User']"}),
            'forcedValues': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'targetOrganizations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['workspace.UserWorkSpace']", 'symmetrical': 'False'}),
        },
        'workspace.workspacevariable': {
            'Meta': {'object_name': 'WorkSpaceVariable'},
            'abstract_variable': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workspace.AbstractVariable']"}),
            'aspect': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'workspace': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workspace.WorkSpace']"}),
        },
    }

    complete_apps = ['workspace']
