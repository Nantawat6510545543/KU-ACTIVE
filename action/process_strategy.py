from abc import ABC, abstractmethod

from . import utils


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

        storage = utils.get_firebase_instance().storage()
        image_file, image_path = self.strategy.get_image_data(form)
        print(f"Image file = {image_file}")
        print(f"Image path = {image_path}")

        # IF picture not in database
        #       put the picture in datasbase
        # 
        #  Then get fire_url
        file_url = ""
        if image_file:
            storage.child(image_path).put(image_file)
            file_url = storage.child(image_path).get_url(None)

        return file_url


class ProcessStrategy(ABC):
    @abstractmethod
    def get_image_data(self, form):
        pass

    # TODO add error for invalid form types


class ProfilePicture(ProcessStrategy):
    def get_image_data(self, form):
        image_file = form.cleaned_data.get('profile_picture')
        image_path = f"Profile_picture/{image_file}"

        return image_file, image_path


# TODO add error for invalid form types
class ActivityPicture(ProcessStrategy):
    def get_image_data(self, form):
        image_file = form.cleaned_data.get('picture')
        image_path = f"Activity_picture/{image_file}"

        return image_file, image_path


# TODO add error for invalid form types
class ActivityBackgroundPicture(ProcessStrategy):
    def get_image_data(self, form):
        image_file = form.cleaned_data.get('background_picture')
        image_path = f"Activity_background_picture/{image_file}"

        return image_file, image_path
