# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [('lock', '0001_initial')]

    operations = [
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('assoc_uid', models.CharField(max_length=100),), ('uid', models.CharField(max_length=50),), ('time', models.CharField(max_length=50),)],
            bases = (models.Model,),
            options = {},
            name = 'Details',
        ),
        migrations.AddField(
            field = models.CharField(default=1, max_length=50),
            preserve_default = False,
            name = 'username',
            model_name = 'user',
        ),
    ]
