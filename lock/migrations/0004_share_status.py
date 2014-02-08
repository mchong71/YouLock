# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [('lock', '0003_auto_20140126_1951')]

    operations = [
        migrations.AddField(
            field = models.CharField(default='pending', max_length=10),
            preserve_default = False,
            name = 'status',
            model_name = 'share',
        ),
    ]
