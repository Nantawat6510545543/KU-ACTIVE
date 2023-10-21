from django import forms
from django.contrib.auth.forms import UserCreationForm

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
            'bio'
        ]


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture']


class ActivityForm(forms.ModelForm):
    date = pub_date = end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Activity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name in Activity._meta.get_fields():
                field.label = Activity._meta.get_field(field_name).verbose_name
