# Generated by Django 4.2.6 on 2023-10-12 14:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0005_rename_participation_limit_activity_participant_limit_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Participation date')),
                ('participated', models.BooleanField(default=False)),
                ('favorited', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 11, 14, 41, 8, 898473, tzinfo=datetime.timezone.utc), verbose_name='Date of Activity'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 11, 14, 41, 8, 898473, tzinfo=datetime.timezone.utc), verbose_name='Date ended'),
        ),
        migrations.DeleteModel(
            name='Participation',
        ),
        migrations.AddField(
            model_name='activityinteraction',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='action.activity'),
        ),
        migrations.AddField(
            model_name='activityinteraction',
            name='participants',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]
