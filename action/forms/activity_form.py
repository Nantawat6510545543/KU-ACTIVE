from django import forms

from ..models import Activity
from . import utils



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
