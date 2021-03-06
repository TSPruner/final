# Generated by Django 2.0.3 on 2020-02-03 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0018_auto_20200202_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='teamId',
            field=models.IntegerField(choices=[(0, 'Buffalo Bills'), (1, 'Miami Dolphins'), (2, 'New England Patriots'), (3, 'New York Jets'), (4, 'Baltimore Ravens'), (5, 'Cincinnati Bengals'), (6, 'Cleveland Browns'), (7, 'Pittsburgh Steelers'), (8, 'Houston Texans'), (9, 'Indianapolis Colts'), (10, 'Jacksonville Jaguars'), (11, 'Tennessee Titans'), (12, 'Denver Broncos'), (13, 'Kansas City Chiefs'), (14, 'Los Angeles Chargers'), (15, 'Oakland Raiders'), (16, 'Dallas Cowboys'), (17, 'New York Giants'), (18, 'Philadelphia Eagles'), (19, 'Washington Redskins'), (20, 'Chicago Bears'), (21, 'Detroit Lions'), (22, 'Green Bay Packers'), (23, 'Minnestoa Vikings'), (24, 'Atlanta Falcons'), (25, 'Carolina Panthers'), (26, 'New Orleans Saints'), (27, 'Tampa Bay Buccaneers'), (28, 'Arizona Cardinals'), (29, 'Los Angeles Rams'), (30, 'San Francisco 49ers'), (31, 'Seattle Seahawks')], default=0),
        ),
    ]
