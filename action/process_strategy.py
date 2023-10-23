from abc import ABC, abstractmethod
from django.http import HttpRequest

from . import utils

class StrategyContext:
    def __init__(self):
        self.strategy = None

    def set_process(self, strategy: 'ProcessStrategy'):
        if isinstance(strategy, ProcessStrategy):
            self.strategy = strategy
        else:
            raise ValueError("Invalid Strategy for process image!")

    def process_image_url(self, image_file, image_name: str):
        # Process the image and save it to the user
        if self.strategy:
            storage = utils.get_firebase_instance().storage()
            image_file, image_path = self.strategy.get_image_data(image_file, image_name)

            storage.child(image_path).put(image_file)
            file_url = storage.child(image_path).get_url(None)
            return file_url

        else:
            raise ValueError("No Strategy set for process image!")


class ProcessStrategy(ABC):
    @abstractmethod
    def get_image_data(self, request: HttpRequest, image_name: str):
        pass


class ProfilePicture(ProcessStrategy):
    def get_image_data(self, image_file, image_name: str):
        
        image_path = f"Profile_picture/{image_name}"

        return image_file, image_path


class ActivityPicture(ProcessStrategy):
    def get_image_data(self, request: HttpRequest, image_name: str):
        image_file = request.FILES['picture']
        image_path = f"Activity_picture/{image_name}"

        return image_file, image_path


class ActivityBackgroundPicture(ProcessStrategy):
    def get_image_data(self, request: HttpRequest, image_name: str):
        image_file = request.FILES['background_picture']
        image_path = f"Activity_background_picture/{image_name}"

        return image_file, image_path