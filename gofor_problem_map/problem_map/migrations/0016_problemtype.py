# Generated by Django 3.0.4 on 2020-05-02 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem_map', '0015_auto_20200501_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('thematic_field', models.ManyToManyField(to='problem_map.ThematicField')),
            ],
        ),
    ]
