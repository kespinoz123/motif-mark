#!/usr/bin/env python

import cairo

FIGURE_NAME = "Figure_1"

WIDTH = 700
HEIGHT = 700


# Creating Surface
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)

#Create cairo.Context object as "cr"
cr = cairo.Context(surface)


# ------- Adding a Rectangle ----------
# Pink Solid Color
cr.set_source_rgb(0.9, 0.0, 0.9)

# Creating a rectangle: (x, y, w, h)
cr.rectangle(250,300, # position
             300, 150) # width and height
cr.fill() 


# ------- Adding a Line ----------

#start position
cr.move_to(250, 300)

# end position of line from start position
cr.line_to(550, 450)

# cyan color line
cr.set_source_rgb(0, 1, 1)  
cr.set_line_width(4)
cr.stroke()

# ------- Adding Text ----------
#Define font style
cr.select_font_face("Arial",
                    cairo.FONT_SLANT_NORMAL,
                    cairo.FONT_WEIGHT_NORMAL)

#Define the size
cr.set_font_size(30)

#pretty purple
cr.set_source_rgb(0.5, 0.2, 1) 

#Define position (x, y)
cr.move_to(200,230)

#Add text to context
cr.show_text("Figure 1: Rectangle + Line :) ")


# ------- Saving Figure/File to PNG Format ----------

surface.write_to_png(f"{FIGURE_NAME}.png") 