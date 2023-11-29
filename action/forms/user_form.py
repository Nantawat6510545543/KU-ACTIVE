from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm

from action.models import User
from action import utils


def changed_username_is_not_unique(cleaned_data, user_id) -> bool:
    """
    Check if the changed username is already used by another existing user.

    Args:
        cleaned_data (dict): A dictionary containing form field values.
        user_id (int): The ID of the user being edited.

    Returns:
        bool: True if the changed username is not unique, False otherwise.
    """
    user_account = User.objects.filter(username=cleaned_data.get('username'))

    # If the username has been changed, check if it's unique
    return user_account.exclude(pk=user_id).exists()


class UserForm(UserCreationForm):
    """Form for creating user accounts."""

    profile_picture = background_picture = forms.ImageField(required=False)

    class Meta:
        model = None
        fields = [
            'username',
            'password1',
            'XXpassword2XX',
            'email',
            'first_name',
            'last_name',
            'bio',
            'profile_picture',
            'background_picture'
        ]

    def clean(self) -> dict[str, Any]:
        """Clean and validate the form data."""
        cleaned_data = super().clean()

        if changed_username_is_not_unique(cleaned_data, self.instance.id):
            raise forms.ValidationError('Username already exists.')

        # Handle the picture
        image_file = self.cleaned_data.get('profile_picture')
        cleaned_data['profile_picture'] = utils.image_to_base64(image_file)

        background_image_file = self.cleaned_data.get('background_picture')
        cleaned_data['background_picture'] = utils.image_to_base64(background_image_file)
        return cleaned_data
