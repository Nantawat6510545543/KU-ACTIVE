from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Activity, Tag, User
from . import utils


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
        user_account = User.objects.filter(
            username=cleaned_data.get('username'))

        # If the username has been changed, apply validation
        if user_account.exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Username already exists.')

        # Handle the profile picture
        image_file = self.cleaned_data.get('profile_picture')
        cleaned_data['profile_picture'] = utils.image_to_base64(image_file)
        return cleaned_data


class UserEditForm(UserChangeForm):
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio'
        ]

    def clean(self):
        cleaned_data = super().clean()
        user_account = User.objects.filter(
            username=cleaned_data.get('username'))

        if user_account.exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Username already exists.')

        return cleaned_data


class ActivityForm(forms.ModelForm):
    date = pub_date = end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    picture = forms.FileField(required=False)
    background_picture = forms.FileField(required=False)

    class Meta:
        model = Activity
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean() 

        # # Set the activity's picture attribute
        image_file = self.cleaned_data.get('picture')
        cleaned_data['picture'] = utils.image_to_base64(image_file)

        # # Set the activity's background picture attribute
        image_file = self.cleaned_data.get('background_picture')
        cleaned_data['background_picture'] = utils.image_to_base64(
            image_file)

        return cleaned_data