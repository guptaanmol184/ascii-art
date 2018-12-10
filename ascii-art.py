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
    intensity_matrix = []
    if method == 'average':
        for i in range(len(pixel_matrix)):
            intensity_row = []
            for j in range(len(pixel_matrix[i])):
                intensity_row.append(sum(pixel_matrix[i][j])//len(pixel_matrix[i][j]))
            intensity_matrix.append(intensity_row)
    return intensity_matrix

def get_character_matrix(intensity_matrix):
    b_string = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    ascii_matrix = []
    for i in range(len(intensity_matrix)):
        ascii_row = []
        for j in range(len(intensity_matrix[i])):
            mapped_char_index = (intensity_matrix[i][j]/256) * len(b_string)
            ascii_row.append(b_string[int(mapped_char_index)])
        ascii_matrix.append(ascii_row)
    return ascii_matrix


im = Image.open(sys.argv[1])
print('Image successfully loaded.')
im = resize_image(im)
print('Image size: {} x {} '.format(im.width, im.height))

im_mat = get_image_matrix(im)
intensity_mat = get_intensity_matrix(im_mat)
ascii_mat = get_character_matrix(intensity_mat)

for row in ascii_mat:
    for char in row:
        print(char*3, end='')
    print()
