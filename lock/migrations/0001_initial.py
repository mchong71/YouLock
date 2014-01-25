# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = []

    operations = [
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('uid', models.CharField(unique=True, max_length=50),), ('assoc_uid', models.CharField(max_length=100),), ('status', models.BooleanField(default=0),)],
            bases = (models.Model,),
            options = {},
            name = 'Status',
        ),
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('uid', models.CharField(unique=True, max_length=50),), ('first_name', models.CharField(max_length=50),), ('last_name', models.CharField(max_length=50),)],
            bases = (models.Model,),
            options = {},
            name = 'User',
        ),
    ]
