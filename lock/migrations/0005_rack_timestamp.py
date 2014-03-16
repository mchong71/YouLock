# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [('lock', '0004_share_status')]

    operations = [
        migrations.AddField(
            field = models.CharField(default=1, unique=True, max_length=50),
            preserve_default = False,
            name = 'timestamp',
            model_name = 'rack',
        ),
    ]
