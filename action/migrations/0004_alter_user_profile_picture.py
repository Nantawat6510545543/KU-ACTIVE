# Generated by Django 4.2.6 on 2023-10-20 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0003_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.URLField(blank=True, default='', max_length=500),
        ),
    ]
