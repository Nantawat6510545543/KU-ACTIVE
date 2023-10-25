from abc import ABC, abstractmethod
from decouple import config

from .utils import firebase_utils as fu


class StrategyContext:
    def __init__(self):
        self.strategy = None

    def set_process(self, strategy: 'ProcessStrategy'):
        if isinstance(strategy, ProcessStrategy):
            self.strategy = strategy
        else:
            raise ValueError("Invalid Strategy for process image!")

    # Rename method to upload_image() + get_image_url()
    # Pass as (self, form, image_name) no request
    def upload_and_get_image_url(self, form):
        # Process the image and save it to the user
        if self.strategy is None:
            raise ValueError("No Strategy set for process image!")

        storage = fu.get_firebase_instance().storage()
        image_file, image_path = self.strategy.get_image_data(form)
        print(f"Image file = {image_file}")
        print(f"Image path = {image_path}")

        # TODO extract method
        # Check if the file exists
        try:
            # Attempt to get the URL of the file (checks if it exists)
            file_url = storage.child(image_path).get_url(None)
            print(f"FILE = {file_url}")
        except Exception as e:
            print(f"The file at {image_path} does not exist or an error occurred. Uploading the file...")

            if image_file:
                # Upload the file
                storage.child(image_path).put(image_file)

                # Get the URL of the uploaded file
                file_url = storage.child(image_path).get_url(None)
                print(f"The file has been uploaded and its URL is: {file_url}")
            else:
                file_url = self.strategy.get_default_url()

        return file_url


class ProcessStrategy(ABC):
    @abstractmethod
    def get_image_data(self, form):
        pass

    @abstractmethod
    def get_default_url(self):
        pass


# TODO add error for invalid form types
class ProfilePicture(ProcessStrategy):
    def get_image_data(self, form):
        image_file = form.cleaned_data.get('profile_picture')
        image_path = f"Profile_picture/{image_file}"

        return image_file, image_path

    def get_default_url(self):
        return config("DEFAULT_PROFILE", default='')


# TODO add error for invalid form types
class ActivityPicture(ProcessStrategy):
    def get_image_data(self, form):
        image_file = form.cleaned_data.get('picture')
        image_path = f"Activity_picture/{image_file}"

        return image_file, image_path

    def get_default_url(self):
        return config("DEFAULT_PICTURE", default='')


# TODO add error for invalid form types
class ActivityBackgroundPicture(ProcessStrategy):
    def get_image_data(self, form):
        image_file = form.cleaned_data.get('background_picture')
        image_path = f"Activity_background_picture/{image_file}"

        return image_file, image_path
    
    def get_default_url(self):
        return config("DEFAULT_BACKGROUND", default='')