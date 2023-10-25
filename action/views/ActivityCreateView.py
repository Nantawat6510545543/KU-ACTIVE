from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from ..forms import ActivityForm
from ..utils import firebase_utils as fb_utils


class ActivityCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ActivityForm
    template_name = 'action/create_activity.html'

    def get_initial(self):
        # Set the initial value for the field
        initial = super().get_initial()
        initial['pub_date'] = timezone.now()
        return initial

    def process_image(self, form):
        # Create an Activity instance and set its attributes
        activity = form.save(commit=False)
        activity.title = self.request.POST['title']
        image_name = f"{activity.title}{activity.id}"
        storage = fb_utils.get_firebase_instance().storage()
        # Add activity picture
        if form.is_valid() and 'picture' in self.request.FILES:
            # Process the image and save it to the user
            image_file = self.request.FILES['picture']
            image_path = f"Activity_picture/{image_name}"

            # Set the activity's picture attribute
            storage.child(image_path).put(image_file)
            file_url = storage.child(image_path).get_url(None)
            activity.picture = file_url

        # Add activity background picture
        if form.is_valid() and 'background_picture' in self.request.FILES:
            # Process the image and save it to the user
            image_file = self.request.FILES['background_picture']
            image_path = f"Activity_background_picture/{image_name}"

            # Set the activity's picture attribute
            storage.child(image_path).put(image_file)
            file_url = storage.child(image_path).get_url(None)
            activity.background_picture = file_url

    def form_valid(self, form):
        self.process_image(form)
        messages.success(self.request, 'Activity created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Render the form with errors if it's invalid
        messages.error(self.request,
                       'Activity creation failed. Please check the form.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Define the URL to redirect to on form success
        return reverse('action:index')
