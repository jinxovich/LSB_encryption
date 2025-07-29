from PIL import Image
import numpy as np

def decode_image(image_path):

    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    pixels = np.array(img)

    binary_message = ''
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            for channel in range(3):
                binary_message += str(int(pixels[row, col, channel]) & 1)

    bytes_data = bytearray()
    for i in range(0, len(binary_message) - 15, 8):
        if i + 8 <= len(binary_message):
            byte = binary_message[i:i+8]
            if i + 16 <= len(binary_message) and binary_message[i:i+16] == '1111111111111110':
                break
            bytes_data.append(int(byte, 2))

    try:
        return bytes_data.decode('utf-8')
    except UnicodeDecodeError:
        return bytes_data.decode('utf-8', errors='ignore')