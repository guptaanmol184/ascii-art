# ascii-art
Image to ascii art generator

Dependencies
- [Pillow](https://pypi.org/project/Pillow/) 
- [Colorama](https://pypi.org/project/colorama/)
- stty from coreutils (should be present)

```
$ ./ascii-art.py --help
usage: ascii-art.py [-h] [-f {average,lightness,luminosity}]
                    [-c {black,red,green,yellow,blue,magenta,cyan,white,rgb}]
                    [-i] [-t THRESHOLD]
                    image

Transform a 3 band JPG image to ascii art.

positional arguments:
  image                 The image to transform.

optional arguments:
  -h, --help            show this help message and exit
  -f {average,lightness,luminosity}, --filter {average,lightness,luminosity}
                        Choose the filter to use.
  -c {black,red,green,yellow,blue,magenta,cyan,white,rgb}, --color {black,red,green,yellow,blue,magenta,cyan,white,rgb}
                        Choose the color of the output.
  -i, --invert          Invert the image. Make more bright areas less bright
                        and less, more.
  -t THRESHOLD, --threshold THRESHOLD
                        Use this argument with color='rgb' to control only
                        hilighted pixels. Threshold is a float between 0 to 1.
                        Set threshold as 1 to color with the dominating color.
                        Default: 0.0.

```

#### Example
![fox](https://raw.githubusercontent.com/guptaanmol184/ascii-art/master/fox.jpg "Fox")
![ascii-fox](https://raw.githubusercontent.com/guptaanmol184/ascii-art/master/ascii-fox.png "ASCII Fox")
