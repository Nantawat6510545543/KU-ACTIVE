from django import forms
from django.contrib.auth.forms import UserCreationForm

from action.models import User
from action import utils

def changed_username_is_not_unique(cleaned_data, user_id):
    user_account = User.objects.filter(
        username=cleaned_data.get('username'))

    # If the username has been changed, check if it's unique
    return user_account.exclude(pk=user_id.instance.pk).exists()


class UserForm(UserCreationForm):
    profile_picture = background_picture = forms.ImageField(required=False)

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
            'profile_picture',
            'background_picture'
        ]

    def clean(self):
        cleaned_data = super().clean()

        if changed_username_is_not_unique(cleaned_data, self.instance.id):
            raise forms.ValidationError('Username already exists.')

        # Handle the picture
        image_file = self.cleaned_data.get('profile_picture')
        cleaned_data['profile_picture'] = utils.image_to_base64(image_file)

        background_image_file = self.cleaned_data.get('background_picture')
        cleaned_data['background_picture'] = utils.image_to_base64(background_image_file)
        return cleaned_data
