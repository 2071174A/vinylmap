# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=128)),
                ('artist', models.CharField(default=b'', max_length=128)),
                ('cover', models.CharField(default=b'', max_length=128)),
                ('cat_no', models.CharField(unique=True, max_length=64)),
                ('label', models.CharField(default=b'', max_length=128)),
                ('genre', models.CharField(default=b'', max_length=64)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.CharField(default=b'', max_length=40)),
                ('link', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='record',
            name='stores',
            field=models.ManyToManyField(to='recordstoreapp.Store'),
            preserve_default=True,
        ),
    ]
