# Generated by Django 3.0.4 on 2020-05-02 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem_map', '0017_problem_related_problem_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='thematic_field',
        ),
    ]
