# Generated by Django 4.2.7 on 2023-11-08 07:09

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profile_picture', models.TextField(blank=True)),
                ('bio', models.TextField(blank=True)),
                ('event_encoder', models.JSONField(blank=True, default=dict)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date published')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Application Deadline')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='Date of Activity')),
                ('last_date', models.DateTimeField(blank=True, null=True, verbose_name='Last date of activity')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('participant_limit', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('place', models.CharField(blank=True, max_length=200, verbose_name='Place')),
                ('full_description', models.TextField(blank=True, verbose_name='Full Description')),
                ('picture', models.TextField(blank=True, default='')),
                ('background_picture', models.JSONField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FriendStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], default=None, max_length=50, null=True)),
                ('is_friend', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Participation date')),
                ('is_participated', models.BooleanField(default=False)),
                ('is_favorited', models.BooleanField(default=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='action.activity')),
                ('participants', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='tags',
            field=models.ManyToManyField(blank=True, to='action.tag'),
        ),
    ]
