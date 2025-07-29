from PIL import Image

def is_valid_image(image_path):

    try:
        with Image.open(image_path) as img:
            return True
    except IOError:
        return False

def get_image_size(image_path):

    with Image.open(image_path) as img:
        return img.size