# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordstoreapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='cat_no',
            field=models.CharField(default=b'', max_length=64),
            preserve_default=True,
        ),
    ]
