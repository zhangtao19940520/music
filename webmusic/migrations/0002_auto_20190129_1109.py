# Generated by Django 2.1.5 on 2019-01-29 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webmusic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collect',
            name='song_id',
            field=models.CharField(max_length=10),
        ),
    ]
