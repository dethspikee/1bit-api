from PIL import Image
import numpy as np


def convert(image, size):
    BYTE_SIZE = 8
    end = 8
    start = 0

    width, height = int(size[0]), int(size[1])
    img = Image.open(image)
    img = img.convert('1', dither=Image.NONE).resize((width, height))
    arr = np.array(img, dtype=int)

    bytelist = []

    for row in range(height):
        for col in range(16):
            bits = ''.join(str(bit) for bit in arr[row][start:end])
            if len(bits) != BYTE_SIZE:
                bits += '0000'
            bits = hex(int(bits, 2))
            bytelist.append(bits)
            start = end
            end += 8
        start = 0
        end = 8
    
    return ','.join(bit for bit in bytelist)
