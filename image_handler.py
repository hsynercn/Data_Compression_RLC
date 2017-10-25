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
        #print('File opened: ', file.name)
    except IOError:
        print('Can\'t open:' + dir)
    finally:
        file.close()
    return image


def comp_ratio_to_performance(comp_ratio):
    return (100 * (1 - comp_ratio))//1

location = ".\\image_samples\\"

file_names = ["biber", "lenna", "ucak", "goldhill"]

result_folder = "res/"

for file_name in file_names:

    if not os.path.isdir(result_folder):
        os.makedirs(result_folder)

    dir = location + file_name + ".bmp"
    my_bitmap = parse_24bit_bmp(read_image(dir))
    converter = PixelConverter.PixelConverter
    mono = converter.rgb_to_monochrome(my_bitmap.r, my_bitmap.g, my_bitmap.b, my_bitmap.width, my_bitmap.height)
    gray_4 = converter.rgb_to_4bit_gray(my_bitmap.r, my_bitmap.g, my_bitmap.b, my_bitmap.width, my_bitmap.height)
    color_255 = converter.rgb_to_255_colortable(my_bitmap.r, my_bitmap.g, my_bitmap.b, my_bitmap.width,
                                                my_bitmap.height)

    plt.imshow(mono, cmap='gray')
    plt.savefig(result_folder +file_name + "_mono.png")
    plt.imshow(gray_4, cmap='gray')
    plt.savefig(result_folder +file_name + "_gray.png")
    plt.imshow(color_255, cmap='gray')
    plt.savefig(result_folder +file_name + "_color.png")

    compression_util = CompressionUtil.CompressionUtil

    data = [mono, gray_4, color_255]
    data_types = [compression_util.EncodingType.MONOCHROME, compression_util.EncodingType.GRAYSCALE_4,
                  compression_util.EncodingType.COLORTABLE_256]
    data_names = ["MONO", "4BIT", "256COLOR"]


    travel = [compression_util.RleTravel.ROW, compression_util.RleTravel.COLUMN, compression_util.RleTravel.ZIGZAG,
              compression_util.RleTravel.ZIGZAG_SEGMENT]

    travel_names = ["ROW", "COLUMN", "ZIGZAG", "ZIGZAG SEGMENT"]

    print("FILE NAME:", file_name)
    for i in range(0, len(data)):
        for j in range(0, len(travel)):
            compressed = compression_util.rle_encode(data[i], my_bitmap.width, my_bitmap.height, travel[j], data_types[i])
            if data_types[i] == compression_util.EncodingType.GRAYSCALE_4:
                comp_ratio = (len(compressed)/2)/(my_bitmap.width * my_bitmap.height)
                print(data_names[i], travel_names[j], " SIZE:", len(compressed)/2, "COMP RATIO:", comp_ratio, "COMP PER"
                      , comp_ratio_to_performance(comp_ratio))
            elif data_types[i] == compression_util.EncodingType.MONOCHROME:
                comp_ratio = (len(compressed)*8)/(my_bitmap.width * my_bitmap.height)
                print(data_names[i], travel_names[j], " SIZE:", len(compressed)*8, "COMP RATIO:", comp_ratio, "COMP PER"
                      , comp_ratio_to_performance(comp_ratio))
            elif data_types[i] == compression_util.EncodingType.COLORTABLE_256:
                comp_ratio = len(compressed)/(my_bitmap.width * my_bitmap.height)
                print(data_names[i], travel_names[j], " SIZE:", len(compressed), "COMP RATIO:", comp_ratio, "COMP PER",
                      comp_ratio_to_performance(comp_ratio))


