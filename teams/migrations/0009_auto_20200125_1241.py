# Generated by Django 2.0.3 on 2020-01-25 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_playerstats'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerstats',
            old_name='funLpst',
            new_name='fumLost',
        ),
    ]
