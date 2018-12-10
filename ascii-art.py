#!/usr/bin/env python

from PIL import Image
from colorama import Fore, Back, Style, init
import sys
import os

# resize to the size i want
def resize_image(im, max_width, max_height):
    im.thumbnail((max_width//3, max_height)) # divide by 3 -> we draw each pixel py 3 letter
    return im

# convert image to 2d matrix
def get_image_matrix(im):
    pixel_list = list(im.getdata())
    pixel_matrix = [pixel_list[i: i+im.width] for i in range(0, len(pixel_list), im.width)]
    return pixel_matrix

# convert 2d image matrix to brightness matrix
def get_intensity_matrix(pixel_matrix, method='average', invert=False):
    if method == 'average':
        intensity_matrix = [[ sum(pixel)//3 for pixel in row] for row in pixel_matrix]
    elif method == 'lightness':
        intensity_matrix = [[ (min(pixel)+max(pixel))//2 for pixel in row] for row in pixel_matrix]
    elif method == 'luminosity':
        intensity_matrix = [[ 0.21*pixel[0] + 0.72*pixel[1] + 0.07*pixel[2] for pixel in row] for row in pixel_matrix]

    if invert:
        return [[ (255-pixel) for pixel in row ] for row in intensity_matrix]
    else:
        return intensity_matrix

# characters in the increasing order of their brightness on the screen
def get_mapped_char(intensity):
    b_string = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    return b_string[int((intensity/256)*len(b_string))]

# returns the 2d matrix representing the ascii image
def get_character_matrix(intensity_matrix):
    return [[get_mapped_char(intensity_val) for intensity_val in row] for row in intensity_matrix ]

# COLORAMA AVAILABLE OPTIONS
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL
def display_ascii_image(ascii_image_matrix, fgcolor='white'):
    if fgcolor == 'white':
        colorstr = Fore.WHITE
    if fgcolor == 'green':
        colorstr = Fore.GREEN
    if fgcolor == 'red':
        colorstr = Fore.RED
    if fgcolor == 'blue':
        colorstr = Fore.BLUE

    f = lambda x: x*3
    # sorry for the cryptic print
    print(*[ colorstr + ''.join([f(ascii_char) for ascii_char in row]) for row in ascii_image_matrix], sep='\n')
    # return terminal to normal state
    print(Style.RESET_ALL)

    #for row in ascii_mat:
    #    for char in row:
    #        print(char*3, end='')
    #    print()

def main():
    # set up max size
    if not('LINES' in os.environ or 'COLUMNS' in os.environ):
        # cannot get lines and columns, define default
        print('export LINES and COLUMNS environment variables before running this script if possible,'+
                'or else we use predefined default values')
        columns = 680
        lines = 105
    else:
        print('Got values from env, lines:', os.environ['LINES'], ' columns:', os.environ['COLUMNS'])
        columns = int(os.environ['COLUMNS'])
        lines = int(os.environ['LINES'])

    im = Image.open(sys.argv[1])
    print('Image successfully loaded.')
    im = resize_image(im, columns, lines)
    print('Image size: {} x {} '.format(im.width, im.height))

    # processing
    im_mat = get_image_matrix(im)
    intensity_mat = get_intensity_matrix(im_mat, 'luminosity')
    ascii_mat = get_character_matrix(intensity_mat)
    display_ascii_image(ascii_mat, 'green')

if __name__ == '__main__':
    init() # initialize colorama
    main()
