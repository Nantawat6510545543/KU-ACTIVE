from datetime import datetime
from typing import Any
from django import forms
from django.utils import timezone
from action.forms.multiple_file import MultipleFileField

from action.models import Activity
from action import utils


def not_datetime(cleaned_data) -> bool:
    """
    Check if any of the specified date fields in cleaned_data are not instances of datetime.

    Args:
        cleaned_data (dict): A dictionary containing form field values.

    Returns:
        bool: True if any specified date field is not an instance of datetime, False otherwise.
    """
    date_type_list = ['pub_date', 'end_date', 'start_date', 'last_date']

    for each_date_type in date_type_list:
        date = cleaned_data.get(each_date_type)
        if not isinstance(date, datetime):
            return True
    return False


def activity_is_newly_created(activity_id) -> bool:
    """
    Check if the activity with the given ID exists in the database.

    Args:
        activity_id (int): The ID of the activity to check.

    Returns:
        bool: True if the activity with the given ID does not exist, False otherwise.
    """
    return not Activity.objects.filter(id=activity_id).exists()


def pub_date_is_less_than_today(cleaned_data) -> bool:
    """
    Check if the Publication Date is earlier than today.

    Args:
        cleaned_data (dict): A dictionary containing form field values.

    Returns:
        bool: True if the Publication Date is earlier than today, False otherwise.
    """
    pub_date = cleaned_data.get('pub_date')
    return pub_date.date() < timezone.now().date()


def end_date_and_pub_date_difference_less_than_1_hour(pub_date, end_date) -> bool:
    """
    Check if the difference between Application Deadline and Publication Date is less than 1 hour.

    Args:
        pub_date (datetime): Publication Date.
        end_date (datetime): Application Deadline.

    Returns:
        bool: True if the time difference is less than 1 hour, False otherwise.
    """
    time_difference = end_date - pub_date
    return time_difference.total_seconds() < 3600


def get_background_data(cleaned_data, activity_id) -> dict[str, str]:
    """
    Get background data based on the cleaned_data and activity_id.

    Args:
        cleaned_data (dict): A dictionary containing form field values.
        activity_id (int): ID of the activity.

    Returns:
        dict: base64-encoded background data.
    """
    background_file = cleaned_data.get('background_picture')
    existing_activity = Activity.objects.filter(id=activity_id)

    if background_file is None and existing_activity.exists():
        return existing_activity[0].background_picture

    return utils.background_image_to_base64(background_file)


class ActivityForm(forms.ModelForm):
    """Form for creating and updating activities."""

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

    def clean(self) -> dict[str, Any]:
        """Clean and validate the form data."""
        cleaned_data = super().clean()

        pub_date = cleaned_data.get('pub_date')
        end_date = cleaned_data.get('end_date')
        start_date = cleaned_data.get('start_date')
        last_date = cleaned_data.get('last_date')

        if not_datetime(cleaned_data):
            return cleaned_data

        if activity_is_newly_created(self.instance.id) and pub_date_is_less_than_today(
                cleaned_data):
            self.add_error('pub_date', "Publication Date must be at least today.")

        if end_date_and_pub_date_difference_less_than_1_hour(pub_date, end_date):
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
