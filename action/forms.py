from django import forms
from django.contrib.auth.forms import UserCreationForm
from decouple import config

from .models import Activity, Tag, User


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

    # TODO merge into clean()
    def clean_username(self):
        username = self.cleaned_data['username']

        # If the username has been changed, apply validation
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Username already exists.')
        return username

    # TODO รีบแก้ด่วนนนนนนนนน
    # # TODO merge into clean()
    # def clean_profile_picture(self):
    #     data = self.cleaned_data['profile_picture']

    #     if 'profile_picture' in self.changed_data:
    #         data = user new picture
    #     else:
    #         data = user existing picture (URLField)

    #     if not data:
    #         data = config("DEFAULT_BACKGROUND", default='')

    #     return data


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
