# Generated by Django 4.2.7 on 2023-11-05 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0007_alter_activity_background_picture_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='event_encoder',
            field=models.JSONField(blank=True, default={}),
            preserve_default=False,
        ),
    ]