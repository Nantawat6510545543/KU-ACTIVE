import base64
from PIL import Image, UnidentifiedImageError
from io import BytesIO

MAX_SIZE = (1024, 1024)
CONVERT_TYPE = 'RGB'
FORMAT = 'JPEG'
UNICODE = 'utf-8'


def image_to_base64(image_file):
    try:
        img = Image.open(image_file)
        img = img.resize(MAX_SIZE)
        img = img.convert(CONVERT_TYPE)

        img_byte_array = BytesIO()
        img.save(img_byte_array, format=FORMAT)
        image_data = img_byte_array.getvalue()

        base64_encoded = base64.b64encode(image_data).decode(UNICODE)
        return base64_encoded
    except (ValueError, AttributeError, UnidentifiedImageError):
        return ""
    except (FileNotFoundError, OSError):
        return image_file
