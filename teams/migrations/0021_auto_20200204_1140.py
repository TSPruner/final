# Generated by Django 2.0.3 on 2020-02-04 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0020_auto_20200204_1139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='defstats',
            old_name='pctStart',
            new_name='ranking',
        ),
        migrations.RenameField(
            model_name='kickerstats',
            old_name='pctStart',
            new_name='ranking',
        ),
    ]
