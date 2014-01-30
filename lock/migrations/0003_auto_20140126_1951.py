# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [('lock', '0002_auto_20140126_1919')]

    operations = [
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('status', models.CharField(max_length=10),), ('uid', models.CharField(unique=True, max_length=50),)],
            bases = (models.Model,),
            options = {},
            name = 'Rack',
        ),
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('assoc_uid', models.CharField(max_length=100),), ('uid', models.CharField(max_length=50),), ('time', models.CharField(max_length=50),)],
            bases = (models.Model,),
            options = {},
            name = 'Share',
        ),
        migrations.DeleteModel(
            'Status',
        ),
    ]
