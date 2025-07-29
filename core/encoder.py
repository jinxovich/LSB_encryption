from PIL import Image
import numpy as np

def encode_image(image_path, secret_message):

    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    pixels = np.array(img)

    message_bytes = secret_message.encode('utf-8')
    binary_message = ''.join(format(byte, '08b') for byte in message_bytes)
    binary_message += '1111111111111110'
    
    # проверка места
    num_pixels = pixels.shape[0] * pixels.shape[1]
    if len(binary_message) > num_pixels * 3:
        raise ValueError("сообщение слишком длинное")

    index = 0
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            for channel in range(3):  # RGB
                if index < len(binary_message):
                    current_value = int(pixels[row, col, channel])
                    new_value = (current_value & ~1) | int(binary_message[index])
                    pixels[row, col, channel] = np.clip(new_value, 0, 255)
                    index += 1
                else:
                    break
            if index >= len(binary_message):
                break
        if index >= len(binary_message):
            break

    return Image.fromarray(pixels.astype(np.uint8))

def save_encoded_image(encoded_image, output_path):

    if encoded_image.mode != 'RGB':
        encoded_image = encoded_image.convert('RGB')
    
    if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
        encoded_image.save(output_path, 'JPEG', quality=95)
    else:
        encoded_image.save(output_path, 'PNG')