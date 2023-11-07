from django import forms
from django.utils import timezone
from datetime import timedelta

from ..models import Activity
from . import utils


class ActivityForm(forms.ModelForm):
    date_fields = {
        'pub_date': 'Publication Date',
        'end_date': 'Application Deadline',
        'start_date': 'Date of Activity',
        'last_date': 'Last date of activity'
    }

    for field_name, field_label in date_fields.items():
        locals()[field_name] = forms.DateTimeField(
            label=field_label,
            widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            input_formats=['%Y-%m-%dT%H:%M']
        )
    picture = background_picture = forms.ImageField(required=False)

    class Meta:
        model = Activity
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        pub_date = cleaned_data.get('pub_date')
        end_date = cleaned_data.get('end_date')
        start_date = cleaned_data.get('start_date')
        last_date = cleaned_data.get('last_date')

        activity_is_created = Activity.objects.filter(id=self.instance.id)

        if not activity_is_created:
            if pub_date.date() < timezone.now().date():
                self.add_error('pub_date',
                               "Publication Date must be at least today.")

        time_difference = end_date - pub_date
        if time_difference.total_seconds() < 3600:
            self.add_error('end_date',
                           "Application Deadline must be at least 1 hour "
                           "after Publication Date.")

        if start_date < end_date:
            self.add_error('start_date',
                           "Date of Activity must be after "
                           "Application Deadline.")

        if last_date < start_date:
            self.add_error('last_date', "Last Date must be after Start Date.")

        # # Set the activity's picture attribute
        image_file = self.cleaned_data.get('picture')
        cleaned_data['picture'] = utils.image_to_base64(image_file)

        # # Set the activity's background picture attribute
        image_file = self.cleaned_data.get('background_picture')
        cleaned_data['background_picture'] = utils.image_to_base64(
            image_file)

        return cleaned_data
