from django import forms
from django.contrib.auth.forms import UserChangeForm

from action.models import User
from action import utils


class UserEditForm(UserChangeForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
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

        if user_account.exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Username already exists.')

        image_file = self.cleaned_data.get('profile_picture')
        cleaned_data['profile_picture'] = utils.image_to_base64(image_file)
        return cleaned_data
