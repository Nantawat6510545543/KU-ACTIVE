# Generated by Django 4.2.6 on 2023-10-21 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0009_rename_activity_date_activity_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='background_picture',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
