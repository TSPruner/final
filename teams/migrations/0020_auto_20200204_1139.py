# Generated by Django 2.0.3 on 2020-02-04 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0019_auto_20200203_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerstats',
            old_name='pctStart',
            new_name='ranking',
        ),
    ]
