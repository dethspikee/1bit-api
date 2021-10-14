from functools import lru_cache

from PIL import Image
from io import BytesIO
import numpy as np
import base64


@lru_cache(maxsize=512)
def convert(base64image, size, threshold=None):
    BYTE_SIZE = 8
    end = 8
    start = 0

    image = BytesIO(base64.b64decode(base64image))
    width, height = int(size[0]), int(size[1])
    img = Image.open(image).resize((width, height))
    if threshold is None:
        img = img.convert('1', dither=Image.NONE)
    else:
        img = img.convert('L')
        img = img.point(lambda x: 255 if x > int(threshold) else 0)
        img.convert('1')
    arr = np.array(img, dtype=int)

    bytelist = []

    for row in range(height):
        for col in range(16):
            if threshold is not None:
                arr[row][arr[row] == 255] = 1
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
