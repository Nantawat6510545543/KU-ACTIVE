import re
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Activity, Tag, User
from .process_strategy import ActivityBackgroundPicture, ActivityPicture, ProfilePicture, StrategyContext


class ActivityAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Activity
        fields = '__all__'


class UserForm(UserCreationForm):
    profile_picture = forms.FileField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name',
            'bio',
            'profile_picture'
        ]

    def clean(self):
        cleaned_data = super().clean()
        user_account = User.objects.filter(username=cleaned_data.get('username'))

        # If the username has been changed, apply validation
        if user_account.exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Username already exists.')

        # Handle the profile picture
        context = StrategyContext()
        context.set_process(ProfilePicture())
        file_url = context.upload_and_get_image_url(self)

        cleaned_data['profile_picture'] = file_url
        return cleaned_data


class UserEditForm(UserChangeForm):
    password = forms.PasswordInput()
    profile_picture = forms.FileField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'bio',
            'profile_picture'
        ]

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        user_account = User.objects.filter(username=cleaned_data.get('username'))

        # If the username has been changed, apply validation
        # TODO tell this to shut up
        print(f"Instance PK: {self.instance.pk}")

        if user_account.exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Username already exists.')

        # Handle the profile picture if it exists in the request
        context = StrategyContext()
        context.set_process(ProfilePicture())
        file_url = context.upload_and_get_image_url(self)

        cleaned_data['profile_picture'] = file_url
        return cleaned_data


class ActivityForm(forms.ModelForm):
    date = pub_date = end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Activity
        fields = '__all__'

    # TODO merge into clean()
    def clean(self):
        cleaned_data = super().clean()

        context = StrategyContext()
        # # Set the activity's picture attribute
        # if 'picture' in self.request.FILES:
        context.set_process(ActivityPicture())
        cleaned_data['picture'] = context.upload_and_get_image_url(self)

        # # Set the activity's background picture attribute
        # if 'background_picture' in self.request.FILES:
        context.set_process(ActivityBackgroundPicture())
        cleaned_data['background_picture'] = context.upload_and_get_image_url(self)

        return cleaned_data