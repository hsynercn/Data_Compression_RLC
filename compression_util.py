from enum import Enum
import struct

class RleTravel(Enum):
    ROW = 1
    COLUMN = 2
    ZIGZAG = 3
    ZIGZAG_SEGMENT = 4


def grayscale4bit_rle_encode(gray4bit_matrix, width, height, travel_type):
    counter = 0
    frame = bytearray()
    if travel_type == RleTravel.ZIGZAG:
        result = zigzag_sequence(gray4bit_matrix, width, height)
    elif travel_type == RleTravel.ROW:
        result = row_sequence(gray4bit_matrix, width, height)
    else:
        result = row_column(gray4bit_matrix, width, height)
    # bit value of 1 represents white pixels (light on) and a value of 0 the black ones (light off)
    # if first pixel is dark we need to start with zero white
    last_symbol = result[0]
    for i in range(0, len(result)):
        if last_symbol == result[i]:
            counter += 1
            if counter == 16:
                frame.append(counter - 1)
                frame.append(last_symbol)
                counter = 1
        else:
            frame.append(counter)
            frame.append(last_symbol)
            last_symbol = result[i]
            counter = 1
    frame.append(counter)
    return frame


def monochrome_rle_encode(monochrome_matrix, width, height, travel_type):
    counter = 0
    frame = bytearray()
    if travel_type == RleTravel.ZIGZAG:
        result = zigzag_sequence(monochrome_matrix, width, height)
    elif travel_type == RleTravel.ROW:
        result = row_sequence(monochrome_matrix, width, height)
    else:
        result = row_column(monochrome_matrix, width, height)
    # bit value of 1 represents white pixels (light on) and a value of 0 the black ones (light off)
    # if first pixel is dark we need to start with zero white
    if result[0] == 0:
        frame.append(0)
    last_symbol = result[0]
    for i in range(0, len(result)):
        if last_symbol == result[i]:
            counter += 1
            if counter == 256:
                frame.append(counter - 1)
                frame.append(0)
                counter = 1
        else:
            last_symbol = result[i]
            frame.append(counter)
            counter = 1
    frame.append(counter)
    return frame


def zigzag_sequence(matrix, width, height):
    m = width - 1
    n = height - 1
    result = []
    index = 0
    for i in range(0, m + n + 1):
        if i % 2 == 0:
            for x in range(i + 1, 0, -1):  # (int x = i; x >= 0; x--)
                # valid matrix index
                if x <= m and (i - x) <= n:
                    result.append(matrix[x][i - x])
                    index += 1;
        else:
            for x in range(0, i + 1):  # (int x = 0; x <= i; x++)
                if x <= m and (i - x) <= n:
                    result.append(matrix[x][i - x])
                    index += 1;
    return result


def row_sequence(monochrome_matrix, width, height):
    result = []
    index = 0
    for i in range(0, height):
        for j in range(0, width):
            result.append(monochrome_matrix[i][j])
    return result


def row_column(monochrome_matrix, width, height):
    result = []
    index = 0
    for i in range(0, height):
        for j in range(0, width):
            result.append(monochrome_matrix[j][i])
    return result


def monochrome_rle_decode_row(frame, width, height):
    switch = 1
    reconstructed = []
    for i in range(0, len(frame)):
        for j in range(0, frame[i]):
            reconstructed.append(switch)
        if switch == 1:
            switch = 0
        else:
            switch = 1
    print("COMPRESSED LEN", len(frame), "RECONSTRUCTED LEN:", len(reconstructed), "CALCULATED LEN", width * height)
    formatted = []
    for i in range(0, height):
        formatted.append([])
        for j in range(0, width):
            formatted[i].append(reconstructed[i * width + j])
    return formatted


def monochrome_rle_decode_column(frame, width, height):
    switch = 1
    reconstructed = []
    for i in range(0, len(frame)):
        for j in range(0, frame[i]):
            reconstructed.append(switch)
        if switch == 1:
            switch = 0
        else:
            switch = 1
    print("COMPRESSED LEN", len(frame), "RECONSTRUCTED LEN:", len(reconstructed), "CALCULATED LEN", width * height)
    formatted = []
    for i in range(0, width):
        formatted.append([])
        for j in range(0, height):
            formatted[i].append(reconstructed[j * width + i])
    return formatted


def monochrome_check(original, formatted):
    for i in range(0, len(original)):
        for j in range(0, len(original[i])):
            if original[i][j] != formatted[i][j]:
                return False
    return True


def gray_4bit_rle_encode(monochrome_matrix):
    return


def colortable_255(monochrome_matrix):
    return
