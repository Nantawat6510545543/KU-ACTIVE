import base64
from PIL import Image, UnidentifiedImageError
from io import BytesIO

MAX_SIZE = 1024


def image_to_base64(image_file) -> str:
    """
    Convert an image file to a base64-encoded string.

    Args:
        image_file (django.core.files.uploadedfile.InMemoryUploadedFile):
            The image file to be converted. It should be an instance of
            'django.core.files.uploadedfile.InMemoryUploadedFile'.

    Returns:
        A base64-encoded string representing the converted image.

    Raises:
        ValueError: If the image file is not a valid image.
        AttributeError: If the image file is missing required attributes.
        UnidentifiedImageError: If the image cannot be identified.
        FileNotFoundError: If the specified file is not found.
        OSError: If an operating system error occurs during the process.

    Note:
        The function resizes the image to a maximum size of 1024x1024 pixels,
        converts it to RGB format, and then encodes it in base64.

        FileNotFoundError and OSError occur when image file was encoded.
        FileNotFoundError may arise on Windows, while OSError may occur on Mac.
    """
    try:
        img = Image.open(image_file)
    except (ValueError, AttributeError, UnidentifiedImageError):
        # If not a valid image or invalid file type
        return ""
    except (FileNotFoundError, OSError):
        # If the image_file is already encoded or other file-related errors
        return image_file

    img = img.resize((MAX_SIZE, MAX_SIZE))
    img = img.convert('RGB')

    img_byte_array = BytesIO()
    img.save(img_byte_array, format='JPEG')
    image_data = img_byte_array.getvalue()

    base64_encoded = base64.b64encode(image_data).decode('utf-8')
    return base64_encoded


def background_image_to_base64(background_file: list) -> dict[str, str]:
    """
    Convert a list of background files to base64-encoded images.

    Parameters:
    - background_file (list): A list of background files.

    Returns:
    dict: A dictionary where keys are in the format 'background i' and values are
          corresponding base64-encoded images.
    """
    background_image_data = {}
    num = 1

    for image in background_file:
        encoded = image_to_base64(image)
        if encoded != '':
            image_key = f'background {num}'
            background_image_data.update({image_key: encoded})
            num += 1

    return background_image_data
