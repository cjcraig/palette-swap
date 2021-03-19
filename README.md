# palette-swap
Creates a copy of an image where original colors are mapped to new colors.

Currently only use through command line is supported, a graphical interface may be added at some point in the future.
To use, requires a "base" image file. Required and optional arguments can be accessed by passing '-h' or '-help' as a command line argument.

The included file "dummy.txt" is used as a default new palette, which is all half-transparent black. "sample.txt" is also included, and has a few more colors. 

Please make your destination palettes of similar format, where each line is:
R, G, B, A
where R, G, and B are integers from 0 to 255 representing the intended red, green, and blue values (respectively), and A is the alpha (0 fully transparent, 255 fully opaque).

