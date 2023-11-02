# Generated by Django 4.2.7 on 2023-11-02 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0005_alter_activity_participant_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='background_picture',
            field=models.TextField(blank=True, default='', max_length=200000),
        ),
        migrations.AlterField(
            model_name='activity',
            name='picture',
            field=models.TextField(blank=True, default='', max_length=200000),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.TextField(blank=True, max_length=200000),
        ),
    ]