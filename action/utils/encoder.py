import base64
from PIL import Image, UnidentifiedImageError
from io import BytesIO


def image_to_base64(image_file):
    max_size = 1024

    try:
        img = Image.open(image_file)
        img = img.resize((max_size, max_size))
        img = img.convert('RGB')

        img_byte_array = BytesIO()
        img.save(img_byte_array, format='JPEG')
        image_data = img_byte_array.getvalue()

        base64_encoded = base64.b64encode(image_data).decode('utf-8')
        return base64_encoded
    except (ValueError, AttributeError, UnidentifiedImageError):
        return ""
    except (FileNotFoundError, OSError):
        return image_file
