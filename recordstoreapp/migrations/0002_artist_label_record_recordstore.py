# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recordstoreapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('artistID', models.IntegerField(default=0, unique=True)),
                ('names', models.CharField(max_length=128)),
                ('biography', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('labelID', models.IntegerField(default=0, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('bio', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recordID', models.IntegerField(default=0, unique=True)),
                ('catalogueNum', models.IntegerField(default=0)),
                ('names', models.CharField(max_length=128)),
                ('tracks', models.CharField(max_length=128)),
                ('picture', models.ImageField(upload_to=b'')),
                ('ganre', models.CharField(max_length=128)),
                ('releaseDate', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecordStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.URLField()),
                ('record', models.ForeignKey(to='recordstoreapp.Record')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
