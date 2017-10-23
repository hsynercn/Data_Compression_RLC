

class PixelConverter:
    @staticmethod
    def merge_rgb(red, green, blue, width, height):
        """Generates a merged rgb matrix from red, green, blue arrays."""
        merged = []
        for i in range(0, height):
            merged.append([])
            for j in range(0, width):
                merged[i].append([])
                merged[i][j].append(red[i][j])
                merged[i][j].append(green[i][j])
                merged[i][j].append(blue[i][j])
        return merged

    @staticmethod
    def rgb_to_monochrome(red, green, blue, width, height):
        """Transforms red, green, blue arrays to 2d monochrome array"""
        monochrome = []
        for i in range(0, height):
            monochrome.append([])
            for j in range(0, width):
                # bit value of 1 represents white pixels (light on) and a value of 0 the black ones (light off)
                if (red[i][j] + green[i][j] + blue[i][j]) / 3 > 128:
                    monochrome[i].append(1)
                else:
                    monochrome[i].append(0)
        return monochrome

    @staticmethod
    def rgb_to_4bit_gray(red, green, blue, width, height):
        """Transforms red, green, blue arrays to averaged 4 bit gray scale matrix"""
        gray_scale = []
        for i in range(0, height):
            gray_scale.append([])
            for j in range(0, width):
                gray_scale[i].append(((red[i][j] + green[i][j] + blue[i][j]) // 3) // 16)
        return gray_scale

    @staticmethod
    def rgb_to_255_colortable(red, green, blue, width, height):
        """ Bit    7  6  5  4  3  2  1  0
            Data   R  R  R  G  G  G  B  B"""
        color = []
        for i in range(0, height):
            color.append([])
            for j in range(0, width):
                color_r = red[i][j] // 32
                color_g = green[i][j] // 32
                color_b = blue[i][j] // 64
                color[i].append(color_r * 32 + color_g * 4 + color_b)
        return color
