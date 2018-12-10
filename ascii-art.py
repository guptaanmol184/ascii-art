#!/usr/bin/env python

from PIL import Image
import sys

# resize to the size i want
def resize_image(im):
    if im.width>500 or im.height>500:
        aspect_ratio = im.width / im.height
        new_ht = 150
        return im.resize((int(aspect_ratio * new_ht), new_ht))
    else:
        return im

# convert image to 2d matrix
def get_image_matrix(im):
    pixel_list = list(im.getdata())
    pixel_matrix = [pixel_list[i: i+im.width] for i in range(0, len(pixel_list), im.width)]
    return pixel_matrix

# convert 2d image matrix to brightness matrix
def get_intensity_matrix(pixel_matrix, method='average'):
    if method == 'average':
        return [[sum(pixel)//len(pixel) for pixel in row] for row in pixel_matrix]

# characters in the increasing order of their brightness on the screen
def get_mapped_char(intensity):
    b_string = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    return b_string[int((intensity/256)*len(b_string))]

# returns the 2d matrix representing the ascii image
def get_character_matrix(intensity_matrix):
    return [[get_mapped_char(intensity_val) for intensity_val in row] for row in intensity_matrix ]

def display_ascii_image(ascii_image_matrix):
    f = lambda x: x*3
    print(*[''.join([f(ascii_char) for ascii_char in row]) for row in ascii_image_matrix], sep='\n')
    #for row in ascii_mat:
    #    for char in row:
    #        print(char*3, end='')
    #    print()

im = Image.open(sys.argv[1])
print('Image successfully loaded.')
im = resize_image(im)
print('Image size: {} x {} '.format(im.width, im.height))

im_mat = get_image_matrix(im)
intensity_mat = get_intensity_matrix(im_mat)
ascii_mat = get_character_matrix(intensity_mat)
display_ascii_image(ascii_mat)

