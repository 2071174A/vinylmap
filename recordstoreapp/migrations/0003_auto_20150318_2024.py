# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordstoreapp', '0002_artist_label_record_recordstore'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='ganre',
            new_name='genre',
        ),
    ]
