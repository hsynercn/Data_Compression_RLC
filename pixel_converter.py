from enum import Enum


class RleTravel(Enum):
    ROW = 1
    COLUMN = 1
    ZIGZAG = 1
    ZIGZAG_SEGMENT = 1


class BitDepth(Enum):
    MONOCHROME = 1
    GRAYSCALE_4BIT = 4
    COLORTABLE = 255


def merge_rgb(red, green, blue, width, height):

    merged = []
    for i in range(0, height):
        merged.append([])
        for j in range(0, width):
            merged[i].append([])
            merged[i][j].append(red[i][j])
            merged[i][j].append(green[i][j])
            merged[i][j].append(blue[i][j])
    return merged


def rgb_to_monochrome(red, green, blue, width, height):

    monochrome = []
    for i in range(0, height):
        monochrome.append([])
        for j in range(0, width):
            # bit value of 1 represents white pixels (light on) and a value of 0 the black ones (light off)
            if (red[i][j] + green[i][j] + blue[i][j])/3 > 128:
                monochrome[i].append(1)
            else:
                monochrome[i].append(0)
    return monochrome


def rgb_to_4bit_gray(red, green, blue, width, height):

    grayscale = []
    for i in range(0, height):
        grayscale.append([])
        for j in range(0, width):
            grayscale[i].append(((red[i][j] + green[i][j] + blue[i][j])//3)//16)
    return grayscale


def rgb_to_255_colortable(red, green, blue, width, height):
    """ Bit    7  6  5  4  3  2  1  0
        Data   R  R  R  G  G  G  B  B"""
    color = []
    for i in range(0, height):
        color.append([])
        for j in range(0, width):
            color_r = red[i][j]//32
            color_g = green[i][j]//32
            color_b = blue[i][j]//64
            color[i].append(color_r * 32 + color_g * 4 + color_b)
    return color
