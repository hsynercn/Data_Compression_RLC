import os
import struct
from Bitmap24 import Bitmap24
from Bitmap32 import Bitmap32
import pixel_converter as pixel_converter
import compression_util as compression_util
import numpy as np
import matplotlib.pyplot as plt


def parse_24bit_bmp(raw_bit):
    """Converts 24-bit bitmap to RGB matrix, returns matrix"""

    parameters = list(struct.unpack('=' + Bitmap24.struct_map, raw_bit[:Bitmap24.struct_size]))
    my_bitmap = Bitmap24(parameters)
    my_bitmap.parse_image_data(raw_bit[my_bitmap.offset:])
    return my_bitmap


def parse_32bit_bmp(raw_bit):
    """Converts 32-bit bitmap to RGB_Alpha matrix, returns matrix"""

    parameters = list(struct.unpack('=' + Bitmap32.struct_map, raw_bit[:Bitmap32.struct_size]))
    my_bitmap = Bitmap32(parameters)
    print('width:', my_bitmap.width, ' height:', my_bitmap.height, 'compression:', my_bitmap.compression)
    my_bitmap.parse_image_data(raw_bit[my_bitmap.offset:])
    return my_bitmap


def read_image(dir):
    """Reads image data, returns raw bit array"""

    image = None

    try:
        file = open(dir, 'rb')
        image = file.read()
        print('File opened: ', file.name)
    except IOError:
        print('Can\'t open:' + dir)
    finally:
        file.close()
    return image


dir = ".\\image_samples\\lenna.bmp"
my_bitmap = parse_24bit_bmp(read_image(dir))
mono = pixel_converter.rgb_to_monochrome(my_bitmap.r, my_bitmap.g, my_bitmap.b, my_bitmap.width, my_bitmap.height)
gray_4 = pixel_converter.rgb_to_4bit_gray(my_bitmap.r, my_bitmap.g, my_bitmap.b, my_bitmap.width, my_bitmap.height)
color_255 = pixel_converter.rgb_to_255_colortable(my_bitmap.r, my_bitmap.g, my_bitmap.b, my_bitmap.width,
                                                  my_bitmap.height)

compressed_mono_row = compression_util.monochrome_rle_encode(mono, my_bitmap.width, my_bitmap.height,
                                                             compression_util.RleTravel.ROW)
print("MONO ROW SIZE:", len(compressed_mono_row))

compressed_mono_col = compression_util.monochrome_rle_encode(mono, my_bitmap.width, my_bitmap.height,
                                                             compression_util.RleTravel.COLUMN)
print("MONO COLUMN SIZE:", len(compressed_mono_col))

compressed_mono_zigzag = compression_util.monochrome_rle_encode(mono, my_bitmap.width, my_bitmap.height,
                                                                compression_util.RleTravel.ZIGZAG)
print("MONO ZIGZAG SIZE:", len(compressed_mono_zigzag))

# plt.imshow(gray_4, cmap='gray')
# plt.show()

compressed_gray4_zigzag = compression_util.grayscale4bit_rle_encode(gray_4, my_bitmap.width, my_bitmap.height,
                                                                   compression_util.RleTravel.ROW)
print("4BIT ROW SIZE:", len(compressed_gray4_zigzag))

compressed_gray4_zigzag = compression_util.grayscale4bit_rle_encode(gray_4, my_bitmap.width, my_bitmap.height,
                                                                   compression_util.RleTravel.COLUMN)
print("4BIT COLUMN SIZE:", len(compressed_gray4_zigzag))

compressed_gray4_zigzag = compression_util.grayscale4bit_rle_encode(gray_4, my_bitmap.width, my_bitmap.height,
                                                                   compression_util.RleTravel.ZIGZAG)
print("4BIT ZIGZAG SIZE:", len(compressed_gray4_zigzag))

