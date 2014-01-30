# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [('lock', '0001_initial')]

    operations = [
        migrations.DeleteModel(
            'Details',
        ),
        migrations.AddField(
            field = models.CharField(default=1, max_length=50),
            preserve_default = False,
            name = 'time',
            model_name = 'status',
        ),
        migrations.RemoveField(
            name = 'status',
            model_name = 'status',
        ),
    ]
