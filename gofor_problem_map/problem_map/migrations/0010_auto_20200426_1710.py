# Generated by Django 3.0.4 on 2020-04-26 14:10

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem_map', '0009_auto_20200426_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='province',
            name='name',
        ),
        migrations.RemoveField(
            model_name='province',
            name='poly',
        ),
        migrations.AddField(
            model_name='province',
            name='cc_1',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='province',
            name='engtype_1',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='province',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='province',
            name='gid_0',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='province',
            name='gid_1',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='province',
            name='hasc_1',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='province',
            name='name_0',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='province',
            name='name_1',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='province',
            name='nl_name_1',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='province',
            name='type_1',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='province',
            name='varname_1',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]
