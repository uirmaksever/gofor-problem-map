# Generated by Django 3.0.4 on 2020-09-29 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem_map', '0021_auto_20200925_0217'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='birth_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='sex',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]