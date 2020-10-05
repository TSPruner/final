# Generated by Django 2.0.3 on 2020-02-11 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0024_auto_20200206_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonschedule',
            name='currentDay',
            field=models.IntegerField(choices=[(0, 'Thursday'), (1, 'Saturday'), (2, 'Sunday'), (3, 'Monday')], default=0),
        ),
        migrations.AddField(
            model_name='seasonschedule',
            name='currentWeek',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, 'Wild Card'), (19, 'Divisional'), (20, 'Conference'), (21, 'Super Bowl')], default=0),
        ),
    ]
