"""
Module to take in an image and replace pixels of chosen color 'A' with color 'X' instead.
So if an image had pixels of colors A, B, C and we wanted to swap to palette X, Y, Z,
every pixel of color A would change to color X, B to Y, C to Z. Intended for use with
simple and small pixel art files.
"""

import argparse
from math import floor
from PIL import Image, ImageDraw
#-----------------------------------------------------

def get_im_data(image: Image):
    """
    Reads through the image and returns a dictionary:
    keys are the unique colors present in the image,
    values represent the number of occurrences of each color.
    """
    #count occurrences of each color in the image, and return the counts
    #recall that for pillow, an image is: [R, G, B, Alpha],
    #where Alpha = 0 is fully transparent, Alpha = 255 is fully opaque
    colors_present = []
    for color in image.getdata():
        if color not  in colors_present:
            colors_present.append(color)
    return colors_present

def make_palette(base: Image, color_list=None, disp_text=None):
    """
    Given a list of all colors present and a base image for mode and size,
    this function returns an image containing "strips" of each color, one strip per unique color.
    If color_list==None, then we default to generating it using get_im_data.
    """

    palette_size = [300, 200]

    if base is None:
        base = Image.new("RGBA", (len(color_list), 1), (255, 255, 255, 0))

    if color_list is None:
        color_list = get_im_data(base)

    palette_image = Image.new(base.mode, palette_size)

    draw = ImageDraw.Draw(palette_image)

    num_cols = len(color_list)
    col_width = floor(palette_size[0] / num_cols)

    right_shift = 0

    for color in color_list:
        print("Current color: " + str(color))
        draw.rectangle(
            (col_width * right_shift, 0, col_width * (right_shift+1), palette_size[1]),
            fill=color,
            outline=None
        )
        right_shift += 1
    if disp_text:
        draw.text((0, 0), disp_text, fill=(255, 255, 255, 255))
    return palette_image

def load_palette_file(file_location):
    """Accepts a text file with each line reading as r,g,b,a where each is a number
    one sequence per line. Will return a palette image consisting
    """
    colors = []
    with open(file_location, 'r') as file:
        #read through the file one line at a time, extracting into a list of the numbers

        for entry in file:
            line = entry.split(',')
            entry = []
            for val in line:
                #convert each number from string to int, then add to current entry
                entry.append(int(val))
            #add the current entry to the list of colors
            colors.append(tuple(entry))
            print("Read in color: " + str(tuple(entry)))
    #at this point we have a list of colors, so we can make a palette
    return make_palette(None, color_list=colors, disp_text="new palette")

def get_color_map(old_colors, new_colors):
    """
    Takes in the list of old colors and list of new colors,
    and returns a dictionary whose keys are the old colors,
    values are the new colors they should map to.
    """
    color_map = {}
    print("###########  BUILDING COLOR MAP  ###########")
    print("Num olds: " + str(len(old_colors)))
    print("Old colors: " + str(old_colors))
    print("Num news: " + str(len(new_colors)))
    max_colors = len(old_colors)
    for i in range(0, max_colors):
        #if our new palette doesn't have as many colors,
        #we'll leave the rest of the original colors untouched.
        if i > len(new_colors) - 1:
            print("Keeping same color, 'swapping' color " + str(old_colors[i]) +
                  " for " + str(old_colors[i]))
            color_map[old_colors[i]] = old_colors[i]
        else:
            print("Swapping color " + str(old_colors[i]) + " for " + str(new_colors[i]))
            color_map[old_colors[i]] = new_colors[i]

    return color_map

def swap_colors(original: Image, palette):
    """
    Takes in an image and a palette to shift it to,
    and returns an image with colors swapped
    """
    old_pal = make_palette(original)

    old_colors = get_im_data(old_pal)
    new_colors = get_im_data(palette)

    # create a blank image, fully transparent, for us to paint our new picture onto
    new_image = Image.new("RGBA", original.size, (255, 255, 255, 0))

    #get a dict telling us which colors get turned into what
    color_map = get_color_map(old_colors, new_colors)

    old_data = original.load()
    new_data = new_image.load()

    for x_coord in range(new_image.size[0]):
        for y_coord in range(new_image.size[1]):
            new_data[x_coord, y_coord] = color_map[old_data[x_coord, y_coord]]

    return new_image

def parser_helper():
    """
    Function to handle argument parsing.
    """
    parser = argparse.ArgumentParser()

    #required argument, specifies the location of the image to be read in
    parser.add_argument('base_path', help="base image to be read")
    #argument specifying the location of the palette we want to shift towards
    parser.add_argument('new_pal_path', nargs="?", default="dummy.txt",
                        help="path of file containing list of new colors")
    #argument to specify destination of the new file
    parser.add_argument('-dest', '-d', default="swapped_image.png",
                        help="specify output file name (default: 'swapped_image.png'")
    #option to display the palette of the original image
    parser.add_argument('-op', '-origpal', action='store_true',
                        help="display the generated palette for the base image")
    #option to display the new/distination palette
    parser.add_argument('-np', '-newpal', action="store_true",
                        help="display the new palette")
    #option to continue process even when displaying palettes
    parser.add_argument('-long', '-l', action='store_true',
                        help="continue swapping colors when using -op or -np")
    return parser.parse_args()


def main():
    """
    Program gets called from here.
    Necessary Command Line Args:
    1: Base Image File's Path
    2: File path of new palette data OR "-o" to display original palette
    Optional Command Line Args:
    (PLANNED): Custom Color Wheel/Palette
    """
    #set up the parser to handle incoming arguments
    parsed = parser_helper()

    original_image = Image.open(parsed.base_path)

    if parsed.op:
        make_palette(original_image, disp_text="old palette").show()
        if not parsed.long:
            return

    if parsed.np:
        load_palette_file(parsed.new_pal_path).show()
        if not parsed.long:
            return

    new_img_path = parsed.dest

    new_palette = load_palette_file(parsed.new_pal_path)

    #We now have the palette for the original image,
    #and our new palette read in from file.

    new_image = swap_colors(original_image, new_palette)

    new_image.save(new_img_path)#, formats="PNG")

    new_image.show()


if __name__ == "__main__":
    main()
