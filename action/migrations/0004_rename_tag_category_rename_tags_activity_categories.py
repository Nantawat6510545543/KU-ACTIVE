# Generated by Django 4.2.6 on 2023-11-17 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0003_alter_activity_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tag',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='tags',
            new_name='categories',
        ),
    ]
