import struct


class Bitmap32:
    """Class for 24 bit bitmap attiributes"""

    attributeNum = 16
    struct_map = '2sIHHIIiiHHIIiiII'
    struct_size = 54

    def __init__(self, parameters):

        if not isinstance(parameters, list):
            raise Exception('32Bitmap init failed: parameter type not valid!')

        if self.attributeNum != len(parameters):
            raise Exception('32Bitmap init failed: parameter size not valid!')

        self.type = parameters[0]
        self.size = parameters[1]
        self.reserved1 = parameters[2]
        self.reserved2 = parameters[3]
        self.offset = parameters[4]
        self.headerSize = parameters[5]
        self.width = parameters[6]
        self.height = parameters[7]
        self.planes = parameters[8]
        self.bits = parameters[9]
        self.compression = parameters[10]
        self.image_size = parameters[11]
        self.x_resolution = parameters[12]
        self.y_resolution = parameters[13]
        self.n_colours = parameters[14]
        self.important_colours = parameters[15]
        self.r = []
        self.g = []
        self.b = []
        self.alpha = []

    def parse_image_data(self, byte_array):
        pixel_row_size = self.width * 4
        byte_cursor = 0

        i = 0
        while i < self.height:
            rgb = list(struct.unpack('=' + 'BBBB' * self.width, byte_array[byte_cursor: byte_cursor + pixel_row_size]))
            byte_cursor += pixel_row_size
            print("line", i)
            self.r.append(rgb[0::4])
            self.g.append(rgb[1::4])
            self.b.append(rgb[2::4])
            self.alpha.append(rgb[3::4])
            i += 1

        i = 0
        height = self.height - 1
        while i < self.height // 2:
            temp = self.r[i]
            self.r[i] = self.r[height - i]
            self.r[height - i] = temp
            temp = self.g[i]
            self.g[i] = self.g[height - i]
            self.g[height - i] = temp
            temp = self.b[i]
            self.b[i] = self.b[height - i]
            self.b[height - i] = temp
            i += 1

