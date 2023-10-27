import base64


def image_to_base64(image_file):
    if image_file is not None:
        image_data = image_file.read()
        base64_encoded = base64.b64encode(image_data).decode('utf-8')
        return base64_encoded
    return ""
