from django import forms
from django.contrib.auth.forms import UserChangeForm
from action.forms.user_form import changed_username_is_not_unique

from action.models import User
from action import utils


class UserEditForm(UserChangeForm):
    profile_picture = background_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
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
