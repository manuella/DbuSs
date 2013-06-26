#Set up.
import dbus
import math
import os.path
import time
import struct
session = dbus.SessionBus()
gimpProxy = session.get_object('edu.grinnell.cs.glimmer.GimpDBus', 
                                '/edu/grinnell/cs/glimmer/gimp')
gimp =  dbus.Interface(gimpProxy, 'edu.grinnell.cs.glimmer.pdb')

#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:


# *************************************************************************
# *                               BRUSHES                                 *
# *************************************************************************


#Procedure: is_valid_brush
#Parameters: brush, a string
#Purpose: to check to see if the brush exists in GIMP
#Produces: result, True or an error message 
#Preconditions: the string for brush is case-sensitive
#Postconditions: the error message pops up in GIMP and informs you that
#                it does not exist.



def is_valid_brush(brush):
    if (gimp.gimp_brush_is_generated(brush)):
        return True
    #Procedure:
    #Parameters:
    #Purpose:
    #Produces:
    #Preconditions:
    #Postconditions:#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:

def context_get_brush():
    return gimp.gimp_context_get_brush()

#Procedure: context_set_brush
#Parameters: brush, a string
#Purpose: changes GIMP's currently selected brush to the one specified
#Produces: brush, the specified brush
#Preconditions: brush exists in GIMP
#Postconditions: GIMP's current brush is now set to specified brush
def context_set_brush(brush):
    if (not(is_valid_brush(brush))):
        raise TypeError("Invalid parameter: " + brush)
    else:
        gimp.gimp_brushes_set_brush(brush)
        


#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:
#def context_list_brushes():

#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:




# *************************************************************************
# *                               DRAWINGS                                *
# *************************************************************************


#Procedure: drawing_bottom
#Parameters: drawing, a drawing
#Purpose: get the bottom edge of drawing
def drawing_bottom(drawing):
    if(drawing_validate(drawing) == True):
        return drawing_top(drawing) + drawing_height(drawing)
    else:
        raise TypeError("drawing_bottom: Given parameter is not a drawing.")

#Procedure: drawing_brush
#Parameters: drawing, a drawing
#Purpose: get the brush associated with the drawing
#Produces: brush, a string
def drawing_brush (drawing):
    if(drawing_validate(drawing) == True):
        return drawing[3]
    else:
        raise TypeError("drawing_brush: Given parameter is not a drawing.")        


#Procedure: drawing_color
#Parameters: drawing, a drawing
#Purpose: get the color of the drawing
#Produces: type, an RGB color
def drawing_color (drawing):
    if(drawing_validate(drawing) == True):
        return drawing[2]
    else:
        raise TypeError("drawing_color: Given parameter is not a drawing.")        


#Procedure: drawing_compose
#Parameters: list_of_drawings, a list of drawings
#Purpose: create a new drawing by composing the drawings in drawings
#Produces: composed, a drawing
def drawing_compose (list_of_drawings):
    drawings = []
    i = 0
    for x in list_of_drawings:
        drawings.append(list_of_drawings[i])
        i = i + 1
    return ["drawing", "group", drawings]


#Procedure: drawing_ellipse
#Parameters: left, a real number
#            top, a real number
#            width, a postive real number
#            hieght, a postive real number 
#Purpose: create a new drawing that represents an ellipse
#Produces: ellipse, a drawing 
#Preconditions: none 
#Postconditions: when rendered, ellipse will be drawn as a filled ellipse,
#                with the specified left margin, top margin. width and height 
def drawing_ellipse(left, right, width, height):
    return drawing_shape("ellipse", rgb_new(0, 0, 0), "", left,
            right, width, height)


#Procedure: drawing_group
#Parameters: drawing1 .... drawingn, n number of drawings
#Purpose: create a new drawing by composing drawing1...drawingn
#Produces: grouped, a drawing
#Preconditions: there is at least one drawing given as an argument
def drawing_group(*drawings):
    a = 0
    for x in drawings:
        if (drawing_validate(drawings[a]) == True):
            a = a + 1
        else:
            raise TypeError("drawing_group: Given drawing(s) are not" +
                            " valid drawings.")
    drawingsTemp = []
    i = 0
    for x in drawings:
        drawingsTemp.append(drawings[i])
        i = i + 1
    drawings_final = ["drawing", "group"]
    j = 0
    for x in drawings:
        drawings_final.append(drawings[j])
        j = j + 1
    return drawings_final


#Procedure: drawing_group_render
#Parameters: drawing, a drawing
#            image, an image
#Purpose: render drawing on image
#Produces: image, the given image
#Preconditions: image and drawing are both valid
#Postconditions: the given image is modified to include drawing
def drawing_group_render(drawing, image):
    if(drawing_validate(drawing) == True and image_validate(image) == True):
        drawings = drawing_members(drawing)
        i = 0
        for x in drawings:
            drawing_shape_render(drawings[i], image)
            i = i + 1
    else:
        raise TypeError("drawing_group_render: Arguments must be a" +
                        " drawing and an image")            


#Procedure: drawing_height
#Parameters: drawing, a drawing
#Purpose: get the height of a drawing
def drawing_height (drawing):
    if(drawing_validate(drawing) == True):
        return drawing[7]
    else:
        raise TypeError("drawing_height: Given parameter is not a drawing.")
    
    
#Procedure: drawing_hshift
#Parameters: drawing, a drawing
#            factor, a real number
#Purpose: create a new version of drawing that is horizontally shifted
#         by the specified factor
#Produces: shifted, a drawing
#Preconditions: drawing is a valid drawing
#Postconditions: scaled is the same overall "shape", color, and size as
#                drawing, but is shifted to the right by factor
#                or to the left if factor is negative
def drawing_hshift(drawing, factor):
    if(drawing_validate(drawing) == True):
            if(drawing_type(drawing) == "group"):
                shifted = []
                drawings = drawing_members(drawing)
                i = 0
                for x in drawings:
                    shifted.append(drawing_hshift(drawings[i], factor))
                    i = i + 1
                return shifted
            elif(drawing_type(drawing) == "ellipse" or
                 drawing_type(drawing) == "rectangle"):
                shape = drawing_type(drawing)
                return drawing_shape(shape, drawing_color(drawing), 
                                     drawing_brush(drawing),
                                     drawing_left(drawing) + factor,
                                     drawing_top(drawing),
                                     drawing_width(drawing),
                                     drawing_height(drawing))
            else:
                raise TypeError("Unknown drawing type, cannot shift.")        
                
    else:
        raise TypeError("drawing_hscale: arguments must be a valid drawing"
                            + " and a real number as the shift factor")    
    
    
#Procedure: drawing_hscale
#Parameters: drawing, a drawing
#            factor, a real number
#Purpose: create a new version of drawing that is horizontally scaled
#         by the given factor
#Produces: scaled, a drawing
#Preconditions: drawing is a valid drawing
#Postconditions: scaled has the same height and color as drawing, but
#                the width and left margin is scaled by factor
def drawing_hscale(drawing, factor):
    if(drawing_validate(drawing) == True):
        if(drawing_type(drawing) == "group"):
            scaled = []
            drawings = drawing_members(drawing)
            i = 0
            for x in drawings:
                scaled.append(drawing_hscale(drawings[i], factor))
                i = i + 1
            return scaled
        elif(drawing_type(drawing) == "ellipse" or
             drawing_type(drawing) == "rectangle"):
            shape = drawing_type(drawing)
            return drawing_shape(shape, drawing_color(drawing), 
                                 drawing_brush(drawing),
                                 drawing_left(drawing) * factor,
                                 drawing_top(drawing),
                                 drawing_width(drawing) * factor,
                                 drawing_height(drawing))
        else:
            raise TypeError("Unknown drawing type, cannot scale.")        
            
    else:
        raise TypeError("drawing_hscale: arguments must be a valid drawing" +
                        " and a real number as the scale factor")


#Procedure: drawing_join
#Parameters: drawing1, a drawing
#            drawing2, a drawing
#Purpose: create a new drawing by joining drawing1 and drawing2
#Produces: joined, a drawing
#Preconditions: none additional
#Postconditions: when rendered, joined is equivalent to rendering drawing1
#                and then drawing2
def drawing_join(drawing1, drawing2):
    if(drawing_validate(drawing1) == True and 
       drawing_validate(drawing2) == True):
        return drawing_group(drawing1, drawing2)
    else:
        raise TypeError("drawing_join: Parameters must both be drawings.")    
    

#Procedure: drawing_left
#Parameters: drawing, a drawing
#Purpose: find the left edge of the drawing 
#Produces: left, a real
def drawing_left(drawing):
    if(drawing_validate(drawing) == True):
        return drawing[4]
    else:
        raise TypeError("drawing_left: Given parameter is not a drawing.")    


#Procedure: drawing_members
#Parameters: drawing, a drawing
#Purpose: get a list of all the sub-drawings in drawing 
#Produces: sub-drawings, a list of drawings
def drawing_members(drawing):
    if(drawing_validate(drawing) == True):
        if (drawing_type(drawing) == "group"):
            drawing.remove("drawing")
            drawing.remove("group")
            return drawing
        else:
            return drawing
    else:
        raise TypeError("drawing_members: Given parameter is not a drawing.")    


#Procedure: drawing_recolor
#Parameters: drawing, a drawing
#            color, an RGB color
#Purpose: create a new version of drawing that is the given color
#Produces: recolored, a drawing
#Preconditions: drawing is a valid drawing
#Postconditions: recolored is the same overall "shape" but is colored color
def drawing_recolor(drawing, color):
    if(drawing_validate(drawing) == True):
            if(drawing_type(drawing) == "group"):
                recolored = []
                drawings = drawing_members(drawing)
                i = 0
                for x in drawings:
                    recolored.append(drawing_recolor(drawings[i], color))
                    i = i + 1
                return recolored
            elif(drawing_type(drawing) == "ellipse" or
                 drawing_type(drawing) == "rectangle"):
                shape = drawing_type(drawing)
                return drawing_shape(shape, color, 
                                     drawing_brush(drawing),
                                     drawing_left(drawing),
                                     drawing_top(drawing),
                                     drawing_width(drawing),
                                     drawing_height(drawing))
            else:
                raise TypeError("Unknown drawing type, cannot recolor.")        
                
    else:
        raise TypeError("drawing_recolor: arguments must be a valid drawing"
                            + " and a color (RGB)") 


#Procedure: drawing_rectangle 
#Parameters: left, an integer
#            top, an integer
#            width, a positive integer
#            hieght, a postive integer
#Purpose: create a new drawing that represents a rectangle 
#Produces: rectangle, a drawing 
#Preconditions: none additional
#Postconditions: when rendered, rectangle will be drawn as a filled rectangle,
#                with the specified left margin, top margin. width and height 
def drawing_rectangle(left, right, width, height):
    return drawing_shape("rectangle", rgb_new(0, 0, 0), "", left,
            right, width, height)


#Procedure: drawing_render
#Parameters: drawing, a drawing
#            image, an image
#Purpose: render the drawing on image
#Produces: image, the given image
#Preconditions: image and drawings are both valid
#Postconditions: image has drawing on it
def drawing_render(drawing, image):
    if(drawing_validate(drawing) == True and image_validate(image) == True):
        if(drawing_type(drawing) == "group"):
            drawing_group_render(drawing, image)
        elif(drawing_type(drawing) == "ellipse" or 
             drawing_type(drawing) == "rectangle"):
            drawing_shape_render(drawing, image)
        else:
            raise StandardError("Drawing cannot be rendered.")
        return image
    else:
        raise TypeError("drawing_render: Arguments must be a drawing" +
                        " and an image")         


#Procedure: drawing_scale
#Parameters: drawing, a drawing
#            factor, a real number
#Purpose: create a new version of drawing that is scaled by the specified
#         factor
#Produces: scaled, a drawing
#Preconditions: drawing is a valid drawing
#Postconditions: scaled is the same overall "shape" and color as drawing
#                but is larger or smaller based on factor's value
def drawing_scale(drawing, factor):
    if(drawing_validate(drawing) == True):
        if(drawing_type(drawing) == "group"):
            scaled = []
            drawings = drawing_members(drawing)
            i = 0
            for x in drawings:
                scaled.append(drawing_scale(drawings[i], factor))
                i = i + 1 
            return scaled
        elif(drawing_type(drawing) == "ellipse" or
             drawing_type(drawing) == "rectangle"):
            shape = drawing_type(drawing)
            return drawing_shape(shape, drawing_color(drawing), 
                                 drawing_brush(drawing),
                                 drawing_left(drawing) * factor,
                                 drawing_top(drawing) * factor,
                                 drawing_width(drawing) * factor,
                                 drawing_height(drawing) * factor)
        else:
            raise TypeError("Unknown drawing type, cannot scale.")
    else:
        raise TypeError("drawing_scale: Given parameter is not a drawing.")  


#Procedure: drawing_shape
#Parameters: type, a string
#            color. rgb color
#            brush, a string 
#            left, an integer
#            top, an integer
#            width, a postive integer
#            height, a postive integer
#Purpose: create one of the shape drawings
#Produces: shape, a drawing
#Preconditions: none additional
#Postconditions: 
#               drawing_type (drawing) = type
#               drawing_color (drawing) = color
#               drawing_left (drawing) = left 
#               drawig_top (drawing) = left 
#               drawing_width (drawing) = width
#               drawing_height (drawing) = height 
def drawing_shape(type, color, brush, left, top, width, height):
    return ["drawing", type, color, brush, left, top, width, height]


#Procedure: drawing_shape_render
#Parameters: drawing, a drawing
#            image, an image
#Purpose: render drawing on image
#Produces: nothing, called for side-effect
#Preconditions: image is a valid image
#               drawing is a valid drawing
#Postconditions: image has been extended by the appropriate drawing
def drawing_shape_render(drawing, image):
    if(drawing_validate(drawing) == True and image_validate(image) == True):
        if(drawing_type(drawing) == "ellipse"):
            image_select_ellipse(image, "REPLACE", drawing_left(drawing),
                                 drawing_top(drawing), drawing_width(drawing),
                                 drawing_height(drawing))
        elif(drawing_type(drawing) == "rectangle"):
            image_select_rectangle(image, "REPLACE", drawing_left(drawing),
                               drawing_top(drawing), drawing_width(drawing),
                               drawing_height(drawing)) 
        context_set_fgcolor(drawing_color(drawing))
        image_fill_selection(image)
        image_select_none(image)
    else:
        raise TypeError("drawing_shape_render: Arguments must be a drawing"
                        + "and an image")             


#Procedure: drawing_top
#Parameters: drawing, a drawing
#Purpose: find the top edge of the drawing
#Produces: top, a real
def drawing_top (drawing):
    if(drawing_validate(drawing) == True):
        return drawing[5]
    else:
        raise TypeError("drawing_top: Given parameter is not a drawing.")       


#Procedure: drawing_type
#Parameters: drawing, a drawing
#Purpose: get the type of drawing
#Produces: type, a string
def drawing_type (drawing):
    if(drawing_validate(drawing) == True):
        return drawing[1]
    else:
        raise TypeError("drawing_type: Given parameter is not a drawing.")     

    
#Procedure: drawing_unit_circle
#Parameters:none
#Purpose: create a circle with diameter of 1
def drawing_unit_circle():
    return drawing_ellipse(0, 0, 1, 1)


#Procedure: drawing_unit_rectangle
#Parameters:none
#Purpose: create a rectangle with edge-lenght of 1
def drawing_unit_square():
    return drawing_rectangle(0, 0, 1, 1)


#Procedure: drawing_type_validate
#Parameters: drawing_type, a string
#Purpose: to check to see if the given type is either "ellipse" or
#         "rectangle"
#Produces: result, a boolean
#Preconditions: drawing_type is the type (or 2nd index) of a drawing
def drawing_type_validate(drawing_type):
    if(drawing_type == "ellipse" or
       drawing_type == "rectangle"):
        return True
    else:
        return False


#Procedure: drawing_validate
#Parameters: drawing, a value
#Purpose: determine whether drawing can be interpreted as a drawing
#Produces: result, a boolean
def drawing_validate(drawing):
    if(drawing[0] == "drawing"):
        if(drawing[1] == "ellipse" or drawing[1] == "rectangle"):
            if(len(drawing) != 8 or
               rgb_validate(drawing[2]) == False or
               drawing[3] != "" or
               type(drawing[4]) is not int or
               type(drawing[5]) is not int or
               type(drawing[6]) is not int or
               type(drawing[7]) is not int):
                return False
            else:
                return True
        elif(drawing[1] == "group"):
            #drawing_group checks for valid drawings already.
            return True
    else:
        False


#Procedure: drawing_vshift
#Parameters: drawing, a drawing
#            factor, a real number
#Purpose: create a new version of drawing that is vertically shifted
#         by the specified factor
#Produces: shifted, a drawing
#Preconditions: drawing is a valid drawing
#Postconditions: scaled is the same overall "shape", color, and size as
#                drawing, but is shifted down by factor or up if factor 
#                is negative
def drawing_vshift(drawing, factor):
    if(drawing_validate(drawing) == True):
            if(drawing_type(drawing) == "group"):
                shifted = []
                drawings = drawing_members(drawing)
                i = 0
                for x in drawings:
                    shifted.append(drawing_vshift(drawings[i], factor))
                    i = i + 1
                return shifted
            elif(drawing_type(drawing) == "ellipse" or
                 drawing_type(drawing) == "rectangle"):
                shape = drawing_type(drawing)
                return drawing_shape(shape, drawing_color(drawing), 
                                     drawing_brush(drawing),
                                     drawing_left(drawing),
                                     drawing_top(drawing) + factor,
                                     drawing_width(drawing),
                                     drawing_height(drawing))
            else:
                raise TypeError("Unknown drawing type, cannot shift.")        
                
    else:
        raise TypeError("drawing_vscale: arguments must be a valid drawing"
                            + " and a real number as the shift factor")    


#Procedure: drawing_vscale
#Parameters: drawing, a drawing
#            factor, a real number
#Purpose: create a new version of drawing that is vertically scaled
#         by the given factor
#Produces: scaled, a drawing
#Preconditions: drawing is a valid drawing
#Postconditions: scaled has the same width and color as drawing, but
#                the height and top margin is scaled by factor
def drawing_vscale(drawing, factor):
    if(drawing_validate(drawing) == True):
        if(drawing_type(drawing) == "group"):
            scaled = []
            drawings = drawing_members(drawing)
            i = 0
            for x in drawings:
                scaled.append(drawing_vscale(drawings[i], factor))
                i = i + 1
            return scaled
        elif(drawing_type(drawing) == "ellipse" or
             drawing_type(drawing) == "rectangle"):
            shape = drawing_type(drawing)
            return drawing_shape(shape, drawing_color(drawing), 
                                 drawing_brush(drawing),
                                 drawing_left(drawing),
                                 drawing_top(drawing) * factor,
                                 drawing_width(drawing),
                                 drawing_height(drawing) * factor)
        else:
            raise TypeError("Unknown drawing type, cannot scale.")        
            
    else:
        raise TypeError("drawing_vscale: arguments must be a valid drawing" +
                        " and a real number as the scale factor")


#Procedure: drawing_width
#Parameters: drawing, a drawing 
#Purpose:get the width of drawing
#Produces: width, a real
def drawing_width (drawing):
    if(drawing_validate(drawing) == True):
        return drawing[6]
    else:
        raise TypeError("drawing_width: Given parameter is not a drawing.")  
    
    
    
# *************************************************************************
# *                            HIGHER ORDER                               *
# *************************************************************************


#Procedure: compose
#Parameters: f, a procedure
#            g, a procedure
#Purpose: compose f and g
#Produces: fog, a procedure
#Preconditions: f can be applied to the results by g
#Postconditions: fog(x) = f(g(x))
def compose(f, g):
    def result(x):
        f(g(x))
    return result


#Procedure: l_s (left section)
#Parameters: biproc, a procedure that takes two parameters
#            left, a value
#Purpose: creates a one parameter procedure by filling in the first
#         parameter of biproc
#Produces: unproc, a procedure that takes one parameter
#Preconditions: left is a valid first argument for biproc
#Postconditions: unproc(right) = biproc(left, right)
def l_s(biproc, left):
    def new_proc(right):
        biproc(left, right)
    return new_proc
    

#Procedure: r_s (right section)
#Parameters: biproc, a procedure that takes two parameters
#            right, a value
#Purpose: creates a one parameter procedure by filling in the second
#         parameter of biproc
#Produces: unproc, a procedure that takes one parameter
#Preconditions: right is a valid second argument for biproc
#Postconditions: unproc(left) = biproc(left, right)
def r_s(biproc, right):
    def new_proc(left):
        biproc(left, right)
    return new_proc

# *************************************************************************
# *                               IMAGES                                  *
# *************************************************************************


#Procedure: image_blot
#Parameters: image, an image
#            col, an integer
#            row, an integer
#Purpose: draw a spot at (col,row) using current brush and fg color
#Produces: image, the modified image
#Preconditions: image is a valid image
#               0 <= col must be <= image_width(image)
#               0 <= row must be <= image_height(image)
#Postconditions: image contains an additional spot at (col,row)
#                that spot may not yet be visible
def image_blot(image, col, row):
    if (image_validate(image) == True):
        layer = image_get_layer(image)
        gimp.gimp_paintbrush_default(layer, 2, [col, row])
        

#Procedure: image_draw_line
#Parameters: image, an image
#            col1, a real
#            row1, a real
#            col2, a real
#            row2, a real
#Purpose: to draw a line with the current brush and foreground color
#         starting at (col1,row1) and ending at (col2,row2)
#Produces: image, the modified image
#Preconditions: none
#Postconditions: none
def image_draw_line(image, col1, row1, col2, row2):
    if (image_validate(image) == True):
            layer = image_get_layer(image)  
            gimp.gimp_paintbrush_default(layer, 4, [col1, row1, col2, row2])


#Procedure: image_fill_selection
#Parameters: image, an image
#Purpose: fill image's current selection (in the active layer) with the 
#         current foreground color
#Produces: nothing, called for side-effect
#Preconditions: image is a valid image
#Postconditions: all of the pixels of the selection in the active layer
#                are filled with the current foreground color
#                the fill may not yet be visible
def image_fill_selection(image):
    if (image_validate(image) == True):
        layer = image_get_layer(image)
        gimp.gimp_edit_fill(layer, 0)
    

#Procedure: image_get_layer
#Parameters: image, an image
#Purpose: to get the active layer of the image
#Produces: layer, the active layer
#Preconditions: image is a valid image
#Postconditions: if the image has no active layer an error will be raised.
def image_get_layer(image):
    if (image_validate(image) == True):
        layer = gimp.gimp_image_get_active_layer(image)
        return layer 
    
    
#Procedure: image_height
#Parameters: image, an image
#Purpose: to get the height of the image
#Produces: height, an integer
#Preconditions: image is a valid image
#Postconditions: height is the height of the image
def image_height (image):
    if(image_validate(image) == True):
        return gimp.gimp_image_height(image)
    
    
#Procedure: image_load
#Parameters: name, a string
#Purpose: loads the given image
#Produces: image, an image
#Preconditions: name is a valid name of an image file
#Postconditions: image is an encapuslated image that corresponds to the 
#                image stored in the given file. 
def image_load(name):
    if(os.path.isfile(name) == True):
        image = gimp.gimp_file_load(1, name, name)
        return image
    else:
        raise TypeError(name + " does not exist, cannot load.")
    
    
#Procedure: image_new
#Parameters: width, a positive integer
#            height, a positive integer
#Purpose: to make a new image of width and height, with one layer
#Produces: img, a new image with one layer
#Preconditions: none additional
#Postconditions: a new image pops up in GIMP with a layer whose color
#                corresponds to the bgcolor. Should invalid arguments
#                (non-integers given for width/height, negative
#                integers given for  width/height) be given, an error 
#                should be thrown.
def image_new(width, height):
    if (type(width) is not int):
        raise TypeError("Width must be an integer, given " + str(width))
    elif(type(height) is not int):
        raise TypeError("Height must be an integer, given " + str(height))
    elif (width <= 0):
        raise TypeError("Invalid width: " + str(width))
    elif (height <= 0):
        raise TypeError("Invalid height: " + str(height))
    else:
        img = gimp.gimp_image_new(width, height, 0)
        layer = gimp.gimp_layer_new(img, width, height, 0, "layer", 100, 0)
        gimp.gimp_image_insert_layer(img, layer, 0, 0)
        gimp.gimp_bucket_fill(layer, 1, 0, 100.0, 0.0, 0, 0.0, 0.0)
        return img
    
      
#Procedure: image_select_all
#Parameters: image, an image
#Purpose: select all pixels in the image
#Produces: nothing, calls for nothing 
#Preconditions: image is a valid image 
#Postconditions: all pixels in image have been selected    
def image_select_all(image):
    if(image_validate(image) == True):
        gimp.gimp_selection_all(image)
        

#Procedure: image_clear_selection
#Parameter: image, an image
#Purpose: clears the currect selection in the active layer in the image 
#Produces: image, the same image
#Preconditions: image is a valid image 
#Postconditions:  All pixels inside the currect selection in the image 
#                 are the background color(or transparent if the active 
#                 layer has an alpha channel)
#                 the clear may not yet be visible
def image_clear_selection(image):
    #image_get_layer validates the image
    layer = image_get_layer(image)
    gimp.gimp_edit_clear(layer)
    
    
#Procedure: image_select_ellipse
#Parameters: 
#    image, an image
#    operation, an string of "ADD", "SUBTRACT", "REPLACE", "INTERSECT"
#    left, an integer 
#    top, an integer 
#    width, an integer 
#    height, an integer 
#Purpose: select an ellipse according to the selection mode specified 
#         by operation, inscribed in the rectangle with the given top,
#         left corner, and the given width and height. 
#Produces: nothing, side effect
#Preconditions: image is valid
#               left, top, width, height describe an ellipse
#Postconditions: an ellipse is selected with given dimensions
def image_select_ellipse(image, operation, top, left, width, height):
    if (image_validate_selection(image, operation, top,
                                 left, width, height) == True):
        gimp.gimp_image_select_ellipse (image, selection_op(operation),
                                        left, top, width, height)


#Procedure: image_select_none
#Parameters: image, an image
#Purpose: it deselects any selection on the image
#Produces: deselected_image, an image without any selection
#Preconditions: none additional
#Postconditions: if image_select_none is called without anything 
#                selected there should be no change to the image. 
def image_select_none(image):
    if (image_validate(image) == True):
        gimp.gimp_selection_none(image)
    
    
#Procedure: image_select_rectangle
#Parameters: 
#    image, an image
#    operation, an string of "ADD", "SUBTRACT", "REPLACE", "INTERSECT"
#    left, an integer 
#    top, an integer 
#    width, an integer 
#    height, an integer 
#Purpose: select a rectangle according to the selection mode specified 
#         by operation, with the given top, left corner, and the given 
#         width and height. 
#Produces: nothing, side effect
#Preconditions: image is valid
#               left, top, width, height describe a rectangle
#Postconditions: a rectangle is selected with given dimensions        
def image_select_rectangle(image, operation, top, left, width, height):
    if (image_validate_selection(image, operation, top,
                                    left, width, height) == True):
        gimp.gimp_image_select_rectangle(image, selection_op(operation),
                                        left, top, width, height)
        
        
#Procedure: image_show
#Parameters: image_id, an integer
#Purpose: Displays the image
#Produces: image, the original image
#Preconditions: image must be a valid image
#Postconditions: the image pops up in GIMP
def image_show(image_id):
    if (image_validate(image_id) == True):
        gimp.gimp_display_new(image_id)

        
#Procedure: image_stroke_selection
#Parameters: image, an image
#Purpose: to trace the edge of the selected reigon of the image (in the active
#         layer) using current brush and foreground color
#Produces: image, the updated image
#Preconditions: image is a valid image
#Postconditions: image has been stroked
#                the stroke may not yet be visible
def image_stroke_selection(image):
    if(image_validate(image) == True):
        gimp.gimp_edit_stroke(gimp.gimp_image_get_active_layer(image))        
 
 
#Procedure: image_validate
#Parameters: image, an image
#Purpose: Determine whether or not image is a valid image or not
#Produces: result, a boolean
def image_validate(image):
    if (not (gimp.gimp_image_is_valid(image))):
        raise TypeError(str(image)
                        + " is not an image.")
    else:
        return True 
 
 
#Procedure:image_validate_selection 
#Parameters: 
#    image, an image
#    operation, an string of "ADD", "SUBTRACT", "REPLACE", "INTERSECT"
#    left, an integer 
#    top, an integer 
#    width, an integer 
#    height, an integer 
#Purpose: validate the typical parameters of a selection operation
#Produces: nothing, calls for a side effect 
#Preconditions: if any parameter is invalid it throws an error
#Postconditions: should be safe to create the selection 
def image_validate_selection(image, operation, left, top, width, height):
    if (not (gimp.gimp_image_is_valid)):
        raise TypeError(image + " is not an image.")
    elif (selection_op(operation) == -1):
        raise TypeError(operation + " is not a valid operation.")
    #elif (type(width) is not int or type(height) is not int or
    #      type(top) is not int or type(left) is not int):
    #    raise TypeError("left, top, width, and height must be of type int.")
    elif (width < 1 or height < 1):
        raise ValueError("Width and height must be at least one.")
    elif (left >= image_width(image) or top >= image_height(image) or
          0 >= left + width or 0 >= top + height):
        raise ValueError("Selection is out of bounds.")
    else:
        return True  
    
    
#Procedure: image_width
#Parameters:image, an image
#Purpose: to get the width of the image 
#Produces: width, an integer 
#Preconditions: image is a valid image  
#Postconditions: width is the width of the image
def image_width (image):
    if(image_validate(image) == True):
        return gimp.gimp_image_width(image)   
    

# *************************************************************************
# *                           MISCELLANEOUS                               *
# *************************************************************************
  
    
#Procedure: bound
#Parameters: value, a number
#            lower, a number
#            upper, a number
#Purpose: bound value to the range (lower - uppper, inclusive)
#Produces: bounded, a number
#Preconditions: lower < upper
#Postconditions: none
def bound(value, lower, upper):
    return min(max(value, lower), upper)

#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:

def context_get_fgcolor():
    return gimp.gimp_context_get_foreground()
    


#Procedure: context_undate_displays
#Parameters: none 
#Purpose: flush recent gimp image operations to the graphical user interface 
#Produces: none, calls for a side effect
#Preconditions: none
#Postconditions: all completed image operations should be visible 
def context_update_displays():
    gimp.gimp_displays_flush()
    
    
    
    
#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:
def context_set_fgcolor(color):
    if(rgb_validate(color) == True):
        gimp.gimp_context_set_foreground(color)
        

#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:
def context_set_bgcolor(color):
    if(rgb_validate(color) == True):
        gimp.gimp_context_set_background(color)
 
 
#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:        




#Procedure: selection_op
#Parameters: operation, a potential selection operation, a string
#Purpose: converts operation to one of the selection operations
#Produces: newOp, an integer
#Preconditions: operation is one of "ADD", "SUBTRACT", "INTERSECT", or
#               "REPLACE". 
#Postconditions: If given operation is not on of the selection operations, 
#                -1 is returned. Operation is successful converted otherwise.
def selection_op(operation):
    if (operation == "ADD"):
        newOp = 0
    elif (operation == "SUBTRACT"):
        newOp = 1
    elif (operation == "REPLACE"):
        newOp = 2
    elif (operation == "INTERSECT"):
        newOp = 3
    else:
        newOp = -1
    return newOp



#Procedure:
#   make-flag
# Parameters:
#   [None]
# Purpose:
#   Creates a new "flag" procedure that stores a modifiable Boolean
#   flag.
# Produces:
#   proc, a parameter of zero-or-one parameters
# Postconditions:
#   (proc val) sets the state to val and returns val.
#   (proc) gets the state.  That is, returns the last val for which
#     there was a call to (proc val).  If there was no such call,
#     returns #t.


class Flag:
    status = True 
    def _init_(self):
        self.status = True    
    def set(self,flag):
        self.status = flag and True
    def get(self):
        return self.status

    
context_preserve = Flag()

    
#Procedure: usleep
#Parameters: seconds
#Purpose: pauses for seconds/1,000,000 (microseconds)
#Produces: nothing, called for side-effect
#Preconditions: none
#Postconditions: action is delayed
def usleep(seconds):
    time.sleep(seconds/1000000)
    
# *************************************************************************
# *                               Pixels                                  *
# *************************************************************************


#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:

def image_compute_pixels(image, pos2color):
    if(image_validate(image) == True):
        pos2color = pos2color(col, row)
        return pos2color

                
#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:

def image_get_pixel(image, col, row):
    if(not(image_validate(image) == True)):
        raise TypeError(image + "is not an image")
    elif(row >= image_width(image) or row < 0):
        raise ValueError ("Selction is out of image")
    elif (col >= image_height(image) or col < 0):
        raise ValueError ("Selection is out of range")
    else:
        layer = image_get_layer(image)
        pixel = gimp.gimp_drawable_get_pixel(layer, col, row)
    return pixel

#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:

def image_set_pixel(image, col, row, red, green, blue):
    if(not(image_validate(image) == True)):
        raise TypeError(image + "is not an image")
    elif(row >= image_width(image) or row < 0):
        raise ValueError ("Selction is out of image")
    elif (col >= image_height(image) or col < 0):
        raise ValueError ("Selection is out of range")
    elif(component_validate(red) or component_validate(green) or component_validate(blue)):
        raise TypeError("Red, Green, Blue is not a valide triple")
    else:
        layer = image_get_layer(image)
        pixel = image_get_pixel(image, col, row)
        gimp.gimp_drawable_set_pixel(layer, row, col, pixel[0], [red, green, blue])
    return 1
    
        
        
                
                
        
        
    
        
    
    
    
    
    
# *************************************************************************
# *                                  RGB                                  *
# *************************************************************************


#Procedure: component
#Parameters: value, a number
#Purpose: to must sure rgb component values lie between 0 and 255 inclusive
#Produces: new_value, an integer 
#Preconditpublic variables in pythonions: none
#Postconditions: 0 <= new_value <= 255
def component(value):
    return bound(int(math.floor(value)), 0, 255)


#Procedure: component_validate
#Parameters: value, a number
#Purpose: to see whether or not value is between 0 and 255 inclusive
#Produces: result, a boolean
#Preconditions: none
#Postconditions: none
def component_validate(value):
    if(type(value) is int and 0 <= value <= 255):
        return True
    else:
        return False


#Procedure: rgb_complement
#Parameters: rgb, an RGB color
#Purpose: find the pseduo-complement of rgb
#Produces: new-rgb, an RGB color
#Preconditions: none additional
#Postconditions: the sum of corresponding components of rgb and new-rgb
#                will equal 255.
def rgb_complement(rgb):
    return rgb_new(255 - rgb_red(rgb), 
                   255 - rgb_green(rgb),
                   255 - rgb_blue(rgb))


#Procedure:
#Parameters:
#Purpose: to get the 32 bit integer that DBus can work with
#Produces:
#Precondipublic variables in pythontions:
#Postconditions:
def rgb_convert(r, g, b):
    red = r << 16
    green = g << 8
    blue = b
    rgb = red + green + blue
    return rgb


#Procedure: rgb_blue
#Parameters: rgb, a RGB color
#Purpose: extract the blue component from rgb
#Produces: blue, an integer
#Preconditions: none
#Postconditions: 0 <= blue <= 255
#                rgb = rgb_new(rgb_red(rgb), rgb_green(rgb), rgb_blue(rgb))
def rgb_blue(rgb):
    red = (rgb >> 16) << 16
    green = ((rgb - red) >> 8) << 8
    blue = rgb - red - green
    return blue


#Procedure: rgb_bluer
#Parameters: rgb, an RGB color
#Purpose: produce a bluer version of rgb
#Produces: bluer, an RGB color
#Preconditions: none additional
#Postconditions: rgb_blue(bluer) >= rgb_blue(rgb)
def rgb_bluer(rgb):
    return rgb_new(rgb_red(rgb),
                   rgb_green(rgb),
                   min(255, 32 + rgb_blue(rgb)))


#Procedure: rgb_darker
#Parameters: rgb, an RGB color
#Purpose: compute a darker version of rgb
#Produces: darker, an RGB color
#Preconditions: none additional
#Postconditions: darker is likely to be interpreted as similar to,
#                but darker than rgb.
def rgb_darker(rgb):
    return rgb_new(max(0, rgb_red(rgb) - 16),
                   max(0, rgb_green(rgb) - 16),
                   max(0, rgb_blue(rgb) - 16))


#Procedure: rgb_green
#Parameters: rgb, an RGB value
#Purpose: extract the green component from rgb
#Produces: green, an integer
#Preconditions: none
#Postconditions: 0 <= green <= 255
#                rgb = rgb_new(rgb_red(rgb), rgb_green(rgb), rgb_blue(rgb))
def rgb_green(rgb):
    red = (rgb >> 16) << 16
    green = (rgb - red) >> 8
    return green


#Procedure: rgb_greener
#Parameters: rgb, an RGB color
#Purpose: produce a greener version of rgb
#Produces: greener, an RGB color
#Preconditions: none additional
#Postconditions: rgb_green(greener) >= rgb_green(rgb)
def rgb_greener(rgb):
    return rgb_new(rgb_red(rgb),
                   min(255, 32 + rgb_green(rgb)),
                   rgb_blue(rgb))


#Procedure: rgb_lighter
#Parameters: rgb, an RGB color
#Purpose: compute a lighter version of rgb
#Produces: lighter, an RGB color
#Preconditions: none additional
#Postconditions: lighter is likely to be interpreted as similar to,
#                but lighter than rgb.
def rgb_lighter(rgb):
    return rgb_new(min(255, rgb_red(rgb) + 16),
                   min(255, rgb_green(rgb) + 16),
                   min(255, rgb_blue(rgb) + 16))

# Procedure: rgb_list_to_rgb_int
# Parameters: rgb, a list of r,g, and b components
# Purpose: convert the standard representation to the int representation to
#          send to gimp

def rgb_list_to_rgb_int(rgb):
    return rgb_convert(rgb[0], rgb[1], rgb[2])    

#Procedure: rgb_phaseshift
#Parameters: rgb, an RGB color
#Purpose: phase shift rgb by adding 128 to components less than or equal to
#         128 and subtracting 128 from components greater than 128.
#Produces: shifted, an RGB color
def rgb_phaseshift(rgb):
    return rgb_new((128 + rgb_red(rgb)) % 255,
                   (128 + rgb_green(rgb)) % 255,
                   (128 + rgb_blue(rgb)) % 255)


#Procedure: rgb_to_rgb_list
#Parameters: rgb, an RGB color
#Purpose: extract components and return them in a list
#Produces: rgb-list, an RGB list
#Preconditions: none
#Postconditions: the components of the rgb-list are the same as rgb
def rgb_to_rgb_list(rgb):
    red = rgb_red (rgb)
    green = rgb_green(rgb)
    blue  = rgb_blue (rgb)
    list = [red, green, blue]
    return list


#Procedure: rgb_to_rgb_string
#Parameters: rgb, an RGB color
#Purpose: convert a rgb color into a string that is readable
#Produces: string, a string of the form R/G/B
#Preconditions: color is a valid RGB color
#Postconditions: R is rgb_red(rgb), G is rgb_green(rgb),
#                B is rgb_blue(rgb)
def rgb_to_rgb_string(rgb):
    red = str (rgb_red (rgb)) 
    green = str (rgb_green(rgb))
    blue  = str (rgb_blue (rgb))
    return red + "/" + green + "/"+ blue 
    
    
#Procedure: rgb_new
#Parameters: red, a real number
#            green, a real number
#            blue, a real number
#Purpose: to create a real number
#Produces: rgb, an RGB color
#Preconditions: none
#Postconditions: if a number is not between 0 and 255 inclusive, it
#                bound between 0 and 255 depending on whether the 
#                number given was under 0 or above 255
def rgb_new(red, green, blue):
    r = component(red)
    g = component(green)
    b = component(blue)
    return rgb_convert(r, g, b)
    

#Procedure: rgb_red
#Parameters: rgb, a RGB color
#Purpose: extract the red component from rgb
#Produces: red, an integer
#Preconditions: none
#Postconditions: 0 <= red <= 255
#                rgb = rgb_new(rgb_red(rgb), rgb_green(rgb), rgb_blue(rgb))
def rgb_red(rgb):
    red = rgb >> 16
    return red 
    

#Procedure: rgb_redder
#Parameters: rgb, an RGB color
#Purpose: produce a redder version of rgb
#Produces: redder, an RGB color
#Preconditions: none additional
#Postconditions: rgb_red(redder) >= rgb_red(rgb)
def rgb_redder(rgb):
    return rgb_new(min(255, 32 + rgb_red(rgb)),
                   rgb_green(rgb),
                   rgb_blue(rgb))


#Procedure: rgb_rotate
#Parameters: rgb, an RGB color
#Purpose: compute a rotated version of rgb
#Produces: rotated, an RGB color
def rgb_rotate(rgb):
    return rgb_new(rgb_green(rgb),
                   rgb_blue(rgb),
                   rgb_red(rgb))

    
#Procedure: rgb_validate
#Parameters: value, a integer
#Purpose: determines if value can be interpreted as an RGB color
#Produces: result, a boolean
#Preconditions: none
#Postconditions: if we can apply the various rgb functions on value,
#                then rgb_validate(value) = true, otherwise false.
def rgb_validate(value):
    if(type(value) is int):
        r = (value >> 16)
        red = r << 16
        g = ((value - red) >> 8)
        green = g << 8
        b = value - red - green 
        if (component_validate(r) == True and component_validate(g) == True
            and component_validate(b) == True):
            return True
    else:
        return False    
    
# *************************************************************************
# *                           Turtles                                     *
# *************************************************************************    

#Procedure:
#Parameters:
#Purpose:
#Produces:
#Preconditions:
#Postconditions:
class Turtle:
    world = 0 
    col = 0
    row = 0
    angle = 0
    angle = 0
    pen_down = True
    color = (rgb_new (0, 0, 0))
    brush = "Circle (01)"
    def _init_(self, image):
        self.world = image
    def turtle_import (self, image):
        self.world = image
    def turtle_clone(self, turtle):
        self.world = turtle.world
        self.col = turtle.col
        self.row = turtle.row
        self.angle = turtle.angle
        self.pen_down = turtle.pen_down
        self.color = turtle.color
        self.brush = turtle.brush
    def turtle_down(turtle):
        self.pen_down = True
    def turtle_face(turtle, angle):
        turtle.angle = angle
    def turtle_forward(turtle, distance):
        d2r = math.pi / 180
        temp_rgb = context_get_fgcolor()
        temp_brush = context_get_brush()
        col = turtle.col
        row = turtle.row
        newcol  =  (turtle.col + (distance * (math.cos (turtle.angle * d2r))))
        newrow = (turtle.row + (distance * (math.sin (turtle.angle * d2r))))
        if (not(turtle.brush == context_get_brush())): #Need to write Get_brush
            # e.x.: check context brush: if == turtle, do not change, if !=, change
            context_set_brush(turtle.brush)
        if(not (turtle.color  == context_get_fgcolor())):
            context_set_fgcolor(turtle.color)
        image_draw_line(turtle.world, col, row, newcol, newrow)
        if(context_preserve.get()):
            context_set_fgcolor(temp_rgb)
            context_set_brush(temp_brush)
        turtle.col = newcol
        turtle.row = newrow
        context_update_displays()
        
    def turtle_teleport(self, x, y):
        self.col = x
        self.row = y
    
    def turtle_turn(self, angle):
        self.angle = self.angle + angle % 360 

    def turtle_face(self, angle):
        self.angle = angle % 360
    
    def turtle_up(self):
        self.pen = False
    
    def turtle_world(self):
        return self.world
    
    def turtle_brush(self, brush):
        self.brush = brush
    
    def turtle_color(self, color):
        self.color = color

    
    
        
            



            
            
        
        
        
    
    
    
    

