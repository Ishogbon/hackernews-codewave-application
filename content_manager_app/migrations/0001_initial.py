# Generated by Django 4.2.4 on 2023-08-11 22:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeWaveComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('by', models.CharField(max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('entry_time', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 927480))),
                ('dead', models.BooleanField(default=False)),
                ('kids', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('text', models.TextField(blank=True, null=True)),
                ('parent', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CodeWaveJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('by', models.CharField(max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('entry_time', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 927480))),
                ('dead', models.BooleanField(default=False)),
                ('kids', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CodeWavePoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('by', models.CharField(max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('entry_time', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 927480))),
                ('dead', models.BooleanField(default=False)),
                ('kids', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('parts', models.JSONField(blank=True, null=True)),
                ('descendants', models.IntegerField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CodeWavePollOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('by', models.CharField(max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('entry_time', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 927480))),
                ('dead', models.BooleanField(default=False)),
                ('kids', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('parent', models.IntegerField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CodeWaveStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('by', models.CharField(max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('entry_time', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 927480))),
                ('dead', models.BooleanField(default=False)),
                ('kids', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('url', models.URLField(blank=True, null=True)),
                ('descendants', models.IntegerField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EntryTracker',
            fields=[
                ('item_id', models.IntegerField(unique=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 926482))),
                ('lock', models.CharField(default='X', max_length=1, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='HackerNewsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('by', models.CharField(max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('entry_time', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 927480))),
                ('dead', models.BooleanField(default=False)),
                ('kids', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('text', models.TextField(blank=True, null=True)),
                ('parent', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HackerNewsJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('by', models.CharField(max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('entry_time', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 927480))),
                ('dead', models.BooleanField(default=False)),
                ('kids', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HackerNewsPoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('by', models.CharField(max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('entry_time', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 927480))),
                ('dead', models.BooleanField(default=False)),
                ('kids', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('parts', models.JSONField(blank=True, null=True)),
                ('descendants', models.IntegerField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HackerNewsPollOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('by', models.CharField(max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('entry_time', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 927480))),
                ('dead', models.BooleanField(default=False)),
                ('kids', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('parent', models.IntegerField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HackerNewsStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('by', models.CharField(max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('entry_time', models.DateTimeField(default=datetime.datetime(2023, 8, 11, 23, 35, 5, 927480))),
                ('dead', models.BooleanField(default=False)),
                ('kids', models.JSONField(blank=True, null=True)),
                ('hash', models.CharField(max_length=64)),
                ('url', models.URLField(blank=True, null=True)),
                ('descendants', models.IntegerField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]