import json
import sys
import matplotlib.pyplot
import numpy
import cairo
import math

def next_power_of_2(n: int):
    if n == 0:
        return 1
    return (1 << (n - 1).bit_length())

def hex(color: str):
    if color[0] == '#':
        color = color[1:]
    if len(color) == 3:
        r = int(color[0] + color[0], base=16)
        g = int(color[1] + color[1], base=16)
        b = int(color[2] + color[2], base=16)
    elif len(color) == 6:
        r = int(color[0:2], base=16)
        g = int(color[2:4], base=16)
        b = int(color[4:6], base=16)
    else:
        raise ValueError("Unsupported hex color format")

    return (r / 255.0, g / 255.0, b / 255.0)


PADDING = (50, 150, 50, 50)
BITMAP_BLOCK_PX = (13, 20)
BITMAP_BLOCK_MARGIN = (2, 2)

COLOR_BG = hex('#23272e')
COLOR_FREE = hex('#a5e075')
COLOR_USED = hex('#f14c4c')
COLOR_EMPTY = (.1, .1, .1)

bitmap = json.load(sys.stdin)

bitmap_blocks_width = next_power_of_2(math.floor(math.sqrt(bitmap['memSize'])))
bitmap_blocks_height = math.ceil(bitmap['memSize'] / bitmap_blocks_width)

# generate blank image
image_width = PADDING[0] + bitmap_blocks_width * (BITMAP_BLOCK_PX[0] + BITMAP_BLOCK_MARGIN[0]) + PADDING[2]
image_height = PADDING[1] + bitmap_blocks_height * (BITMAP_BLOCK_PX[1] + BITMAP_BLOCK_MARGIN[1]) + PADDING[3]

image_data = numpy.zeros((image_width, image_height, 4), dtype=numpy.uint8)
surface = cairo.ImageSurface.create_for_data(image_data, cairo.FORMAT_ARGB32, image_width, image_height)
cr = cairo.Context(surface)

# background
cr.set_source_rgb(*COLOR_BG)
cr.paint()

# draw bitmap blocks
for by in range(bitmap_blocks_height):
    for bx in range(bitmap_blocks_width):
        i = (by * bitmap_blocks_width) + bx
        if i >= bitmap['memSize']:
            c = COLOR_EMPTY
        elif bitmap['bitmap'][i] == '0':
            c = COLOR_FREE
        else:
            c = COLOR_USED
        cr.set_source_rgb(*c)
        cr.rectangle(PADDING[0] + bx * (BITMAP_BLOCK_PX[0] + BITMAP_BLOCK_MARGIN[0]),
                     PADDING[1] + by * (BITMAP_BLOCK_PX[1] + BITMAP_BLOCK_MARGIN[1]),
                     BITMAP_BLOCK_PX[0],
                     BITMAP_BLOCK_PX[1])
        cr.fill()

surface.write_to_png('bitmap.png')