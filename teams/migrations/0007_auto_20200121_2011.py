# Generated by Django 2.0.3 on 2020-01-22 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_auto_20200121_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.IntegerField(choices=[(0, 'QB'), (1, 'RB'), (2, 'FB'), (3, 'WR'), (4, 'TE'), (5, 'OL'), (6, 'DEF'), (7, 'PK'), (8, 'P'), (9, 'LS')], default=0),
        ),
    ]