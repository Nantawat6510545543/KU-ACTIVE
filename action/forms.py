from django import forms
from django.contrib.auth.forms import UserCreationForm
from decouple import config

from .models import Activity, Tag, User
from .process_strategy import ProfilePicture, StrategyContext
from utils import firebase_utils as fu


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
        username = cleaned_data.get('username')

        if username:
            # If the username has been changed, apply validation
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Username already exists.')

        image_file = cleaned_data.get('profile_picture')
        print(image_file)
        image_name = f"{self.instance.username}{self.instance.pk}"
        print(image_name)

        storage = fu.get_firebase_instance().storage()
        image_path = f"Profile_picture/{image_name}"

        storage.child(image_path).put(image_file)
        file_url = storage.child(image_path).get_url(None)

        # Handle the profile picture if it exists in the request
        # if image_file:
        #     context = StrategyContext()
        #     context.set_process(ProfilePicture())
        #     profile_picture = context.process_image_url(image_file, image_name)
        # else:
        #     profile_picture = config("DEFAULT_BACKGROUND", default='')

        self.cleaned_data['profile_picture'] = file_url
        print(self.cleaned_data['username'])
        print(self.cleaned_data['profile_picture'])
        return cleaned_data

    # def clean_profile_picture(self):
    #     profile_picture = self.cleaned_data['profile_picture']

    #     if 'profile_picture' in self.changed_data:
    #         profile_picture = user new picture
    #     else:
    #         profile_picture = user existing picture (URLField)

    #     if not data:
    #         profile_picture = config("DEFAULT_BACKGROUND", default='')

    #     return profile_picture


class ActivityForm(forms.ModelForm):
    date = pub_date = end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Activity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name in Activity._meta.get_fields():
                field.label = Activity._meta.get_field(field_name).verbose_name

    # TODO merge into clean()
    def clean_background_picture(self):
        data = self.cleaned_data['background_picture']
        if not data:
            data = config("DEFAULT_BACKGROUND", default='')
        return data
