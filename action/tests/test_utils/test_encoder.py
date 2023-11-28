from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from action.utils import image_to_base64


class EncoderTest(TestCase):
    """Test case for the image_to_base64 function."""

    def test_image_to_base64_valid_image(self):
        """
        Test the image_to_base64 function with a valid image file.

        1. Set up a SimpleUploadedFile with image content.
        2. Call image_to_base64 and assert that the result is not None.
        """
        image_content = b'content_of_your_image_file'
        image_file = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")
        encoded_image = image_to_base64(image_file)
        self.assertIsNotNone(encoded_image)

    def test_image_to_base64_non_image(self):
        """
        Test the image_to_base64 function with a non-image file.

        1. Set up a SimpleUploadedFile with non-image content.
        2. Call image_to_base64 and assert that the result is an empty string.
        """
        non_image_file = SimpleUploadedFile("non_image_file.txt", b'', content_type="text/plain")
        self.assertEqual(image_to_base64(non_image_file), '')

    def test_image_to_base64_encoded_image(self):
        """
        Test the image_to_base64 function with an already encoded image.

        1. Call image_to_base64 with an encoded image.
        2. Assert that the result is the same as the input encoded image.
        """
        image_content = b'content_of_your_image_file'
        image_file = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")
        encoded_image = image_to_base64(image_file)
        self.assertEqual(image_to_base64(encoded_image), encoded_image)
