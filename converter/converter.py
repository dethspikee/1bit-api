from functools import lru_cache

from PIL import Image
from io import BytesIO
import numpy as np
import base64


@lru_cache(maxsize=512)
def convert(base64image, threshold=None):
    """
    Decode image encoded as base64 then convert it to
    1 bit bitmap. Iterate over newly created bitmap
    converting each 8 bits (a byte) to hex. Store each hex
    as string in the bytelist.
    Optionaly 'threshold' parameter can be used to determine
    point of conversion between white / black colors. In this
    case original image is first converted to 8 bit bitmap and then
    threshold value is applied during point conversion.
    Return list of strings representing pixel values (as hex) of the bitmap.

    Parameters
    ----------
    base64image : bytes
        base64 encoded image

    threshold : str
        Value used to determine point of conversion between white / black
        pixels

    Returns
    -------
    List of str hex values encoding each pixel in the bitmap.
    """
    BYTE_SIZE = 8
    WIDTH = 128
    HEIGHT = 64
    end = 8
    start = 0

    image = BytesIO(base64.b64decode(base64image))
    img = Image.open(image).resize((WIDTH, HEIGHT))
    if threshold is None:
        img = img.convert('1', dither=Image.NONE)
    else:
        img = img.convert('L')
        img = img.point(lambda x: 255 if x > int(threshold) else 0)
        img.convert('1')
    arr = np.array(img, dtype=int)

    bytelist = []

    for row in range(HEIGHT):
        # Divide row of 128 pixels into 8 bit chunks
        # In a row of 128 columns there is exactly 16 8-byte chunks so
        # hardcoding '16' here instead of using arithmetic or variable
        for col in range(16):
            if threshold is not None:
                arr[row][arr[row] == 255] = 1
            bits = ''.join(str(bit) for bit in arr[row][start:end])
            bits = hex(int(bits, 2))
            bytelist.append(bits)
            start = end
            end += 8
        start = 0
        end = 8
    
    return ','.join(bit for bit in bytelist)
