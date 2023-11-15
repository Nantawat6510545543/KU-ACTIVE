from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from action.utils import image_to_base64


class EncoderTest(TestCase):
    def test_image_to_base64(self):
        # Test with a valid image file
        image_content = b'content_of_your_image_file'
        image_file = SimpleUploadedFile("test_image.jpg", image_content,
                                        content_type="image/jpeg")
        encoded_image = image_to_base64(image_file)
        self.assertIsNotNone(encoded_image)

        # Test with a non-image file, expect an empty string
        non_image_file = SimpleUploadedFile("non_image_file.txt", b'',
                                            content_type="text/plain")
        self.assertEqual(image_to_base64(non_image_file), '')

        # Test with an encoded image, expect the same encoded image back
        self.assertEqual(image_to_base64(encoded_image), encoded_image)
