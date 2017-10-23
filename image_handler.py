import os
import struct
from Bitmap24 import Bitmap24
from Bitmap32 import Bitmap32
import PixelConverter
import CompressionUtil as CompressionUtil
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
converter = PixelConverter.PixelConverter
mono = converter.rgb_to_monochrome(my_bitmap.r, my_bitmap.g, my_bitmap.b, my_bitmap.width, my_bitmap.height)
gray_4 = converter.rgb_to_4bit_gray(my_bitmap.r, my_bitmap.g, my_bitmap.b, my_bitmap.width, my_bitmap.height)
color_255 = converter.rgb_to_255_colortable(my_bitmap.r, my_bitmap.g, my_bitmap.b, my_bitmap.width,
                                            my_bitmap.height)

compression_util = CompressionUtil.CompressionUtil

compressed_mono_row = compression_util.rle_encode(mono, my_bitmap.width, my_bitmap.height,
                                                  compression_util.RleTravel.ROW,
                                                  compression_util.EncodingType.MONOCHROME)
print("MONO ROW SIZE:", len(compressed_mono_row)/8)


compressed_mono_col = compression_util.rle_encode(mono, my_bitmap.width, my_bitmap.height,
                                                  compression_util.RleTravel.COLUMN,
                                                  compression_util.EncodingType.MONOCHROME)
print("MONO COLUMN SIZE:", len(compressed_mono_col)/8)


compressed_mono_zigzag = compression_util.rle_encode(mono, my_bitmap.width, my_bitmap.height,
                                                  compression_util.RleTravel.ZIGZAG,
                                                  compression_util.EncodingType.MONOCHROME)
print("MONO ZIGZAG SIZE:", len(compressed_mono_zigzag)/8)

# plt.imshow(gray_4, cmap='gray')
# plt.show()


compressed_gray4_row = compression_util.rle_encode(gray_4, my_bitmap.width, my_bitmap.height,
                                                  compression_util.RleTravel.ROW,
                                                  compression_util.EncodingType.GRAYSCALE_4)
print("4BIT ROW SIZE:", len(compressed_gray4_row)/2)


compressed_gray4_col = compression_util.rle_encode(gray_4, my_bitmap.width, my_bitmap.height,
                                                  compression_util.RleTravel.COLUMN,
                                                  compression_util.EncodingType.GRAYSCALE_4)
print("4BIT COLUMN SIZE:", len(compressed_gray4_col)/2)

compressed_gray4_zigzag = compression_util.rle_encode(gray_4, my_bitmap.width, my_bitmap.height,
                                                  compression_util.RleTravel.ZIGZAG,
                                                  compression_util.EncodingType.GRAYSCALE_4)
print("4BIT ZIGZAG SIZE:", len(compressed_gray4_zigzag)/2)


compressed_color255_row = compression_util.rle_encode(color_255, my_bitmap.width, my_bitmap.height,
                                                  compression_util.RleTravel.ROW,
                                                  compression_util.EncodingType.COLORTABLE_256)
print("256COLOR ROW SIZE:", len(compressed_color255_row))


compressed_color255_col = compression_util.rle_encode(color_255, my_bitmap.width, my_bitmap.height,
                                                  compression_util.RleTravel.COLUMN,
                                                  compression_util.EncodingType.COLORTABLE_256)
print("256COLOR COLUMN SIZE:", len(compressed_color255_col))


compressed_color255_zigzag = compression_util.rle_encode(color_255, my_bitmap.width, my_bitmap.height,
                                                  compression_util.RleTravel.ZIGZAG,
                                                  compression_util.EncodingType.COLORTABLE_256)
print("256COLOR ZIGZAG SIZE:", len(compressed_color255_zigzag))
