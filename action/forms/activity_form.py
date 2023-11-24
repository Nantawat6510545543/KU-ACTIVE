from datetime import datetime
from django import forms
from django.utils import timezone

from action.models import Activity
from action import utils

def not_datetime(cleaned_data):
    pub_date = cleaned_data.get('pub_date')
    end_date = cleaned_data.get('end_date')
    start_date = cleaned_data.get('start_date')
    last_date = cleaned_data.get('last_date')

    return not isinstance(pub_date, datetime) or not isinstance(end_date, datetime) or \
        not isinstance(start_date, datetime) or not isinstance(last_date, datetime)

def activity_is_newly_created(activity_id):
    return not Activity.objects.filter(id=activity_id).exists()

def pub_date_is_less_than_today(cleaned_data):
    pub_date = cleaned_data.get('pub_date')
    return pub_date.date() < timezone.now().date()

def end_date_and_pub_date_difference_less_than_1_hour(cleaned_data):
    pub_date = cleaned_data.get('pub_date')
    end_date = cleaned_data.get('end_date')

    time_difference = end_date - pub_date
    return time_difference.total_seconds() < 3600

def get_background_data(cleaned_data, activity_id):
    # Set the activity's background picture attribute
    background_file = cleaned_data.get('background_picture')
    existing_activity = Activity.objects.filter(id=activity_id)

    if background_file is None and existing_activity.exists():
        return existing_activity[0].background_picture

    return utils.background_image_to_base64(background_file)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


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

    picture = forms.ImageField(required=False)
    background_picture = MultipleFileField()

    class Meta:
        model = Activity
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        pub_date = cleaned_data.get('pub_date')
        end_date = cleaned_data.get('end_date')
        start_date = cleaned_data.get('start_date')
        last_date = cleaned_data.get('last_date')

        if not_datetime(cleaned_data):
            return cleaned_data

        if activity_is_newly_created(self.instance.id) and pub_date_is_less_than_today(cleaned_data):
            self.add_error('pub_date', "Publication Date must be at least today.")

        if end_date_and_pub_date_difference_less_than_1_hour(cleaned_data):
            self.add_error('end_date', "Application Deadline must be at least 1 hour "
                           "after Publication Date.")

        if start_date < end_date:
            self.add_error('start_date', "Date of Activity must be after "
                           "Application Deadline.")

        if last_date < start_date:
            self.add_error('last_date', "Last Date must be after Start Date.")

        # Set the activity's picture attribute
        picture_file = self.cleaned_data.get('picture')
        cleaned_data['picture'] = utils.image_to_base64(picture_file)
        cleaned_data['background_picture'] = get_background_data(cleaned_data, self.instance.id)

        return cleaned_data
