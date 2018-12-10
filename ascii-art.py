#!/usr/bin/env python

from PIL import Image
from colorama import Fore, Back, Style, init
import os
import argparse

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
    if fgcolor == 'black':
        colorstr = Fore.BLACK
    if fgcolor == 'red':
        colorstr = Fore.RED
    if fgcolor == 'green':
        colorstr = Fore.GREEN
    if fgcolor == 'yellow':
        colorstr = Fore.YELLOW
    if fgcolor == 'blue':
        colorstr = Fore.BLUE
    if fgcolor == 'magenta':
        colorstr = Fore.MAGENTA
    if fgcolor == 'cyan':
        colorstr = Fore.CYAN
    if fgcolor == 'white':
        colorstr = Fore.WHITE

    f = lambda x: x*3
    # sorry for the cryptic print
    print(*[ colorstr + ''.join([f(ascii_char) for ascii_char in row]) for row in ascii_image_matrix], sep='\n')
    # return terminal to normal state
    print(Style.RESET_ALL)

    #for row in ascii_mat:
    #    for char in row:
    #        print(char*3, end='')
    #    print()

def display_rgb_ascii_image(ascii_image_matrix, pixel_matrix, threshold):
    colorstr = ''
    color_opts = [ Fore.RED, Fore.GREEN, Fore.BLUE ]

    for char_row, pixel_row in zip(ascii_image_matrix, pixel_matrix):
        for char, pixel in zip(char_row, pixel_row):
            pixel = list(pixel)
            max_value = max(pixel)
            max_index = pixel.index(max_value)
            pixel.remove(max_value)
            # we check is the average of the other pixel values
            # is less than some (thresholded value of max pixel_value)[threshold * max_pixel_value]
            # this means the max truly dominates even after thresholding
            if sum(pixel)//2 <= (threshold)*max_value:
                colorstr = color_opts[max_index]
            else:
                colorstr = Style.RESET_ALL
            print(colorstr, char*3, end='', sep='')
        print()

    # return terminal to normal state
    print(Style.RESET_ALL)

# argument parsing helper
def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("{} not in range [0.0, 1.0]".format(x))
    return x

def main():
    parser = argparse.ArgumentParser(description='Transform a 3 band JPG image to ascii art.')
    parser.add_argument('image', help='The image to transform.')
    parser.add_argument('-f', '--filter', choices=['average', 'lightness', 'luminosity'],
            default='average', help='Choose the filter to use.' )
    parser.add_argument('-c', '--color', choices=['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'rgb'],
            default='white', help='Choose the color of the output.' )
    parser.add_argument('-i', '--invert', action="store_true", help='Invert the image. Make more bright areas less bright and less, more.' )
    parser.add_argument('-t', '--threshold', type=restricted_float, default=0.0, 
            help= 'Use this argument with color=\'rgb\' to control only hilighted pixels. Threshold is a float between 0 to 1.\nSet threshold as 1 to color with the dominating color. Default: 0.0.')

    args = parser.parse_args()

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

    im = Image.open(args.image)
    print('Image successfully loaded.')
    im = resize_image(im, columns, lines)
    print('Image size are resize: {} x {} '.format(im.width, im.height))

    # processing
    im_mat = get_image_matrix(im)
    intensity_mat = get_intensity_matrix(im_mat, args.filter, args.invert)
    ascii_mat = get_character_matrix(intensity_mat)
    if args.color == 'rgb':
        display_rgb_ascii_image(ascii_mat, im_mat, args.threshold)
    else:
        display_ascii_image(ascii_mat, args.color)

if __name__ == '__main__':
    init() # initialize colorama
    main()
