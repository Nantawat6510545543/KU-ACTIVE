# Generated by Django 4.2.7 on 2023-11-02 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0004_alter_activity_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='participant_limit',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
    ]
