import bpy
import bmesh
from bpy.props import *
from bpy.types import (Panel, Menu, Operator, PropertyGroup)

import random
import time

##########################################
# Operator Class
##########################################

class LIBR_OT_Generate(bpy.types.Operator):
    bl_idname = "libr.generate"
    bl_label = "Generate"
    bl_description = "Generate books based on settings."
    bl_options = { "REGISTER", "UNDO" }

    regen: BoolProperty(name = "Regeneration", default = False)

    def execute(self, ctx):
        scene = ctx.scene
        libr = scene.library

        # Make sure template collection exists
        try:
            template_collection = bpy.data.collections[libr.books_collection]
        except: template_collection = None
            # self.report({"ERROR"}, "Select the template collection.")
            # return {"CANCELLED"}

        if template_collection is None:
            self.report({"ERROR"}, "Select the template collection.")
            return {"CANCELED"}
        else:
            for obj in bpy.context.selected_objects:
                obj.select_set(False)

            # All book generation
            tStart = time.time()
            if not self.regen:
                generateBooks(ctx, template_collection)
            else:
                regenerateBooks(ctx, template_collection)
            print("Generation time: {0}s".format(time.time() - tStart))
        
        return {"FINISHED"}

##########################################
# Object Helpers
##########################################

# Regenerate books if it is regenerated
def regenerateBooks(ctx, templates):
    bookshelf = bpy.data.collections['Bookshelf']

    for i in bookshelf.all_objects:
        i.select_set(True)
    bpy.ops.object.delete()

    generateBooks(ctx, templates)

# The main book generating function
def generateBooks(ctx, templates):
    scene = ctx.scene
    libr = scene.library

    cols = libr.shelf_columns
    rows = libr.shelf_rows
    col_width = libr.shelf_column_width
    row_width = libr.shelf_row_width

    # If bookshelf collection doesn't exist then create it and add it to the collection
    try:
        bookshelf = bpy.data.collections["Bookshelf"]
    except:
        bookshelf = bpy.data.collections.new("Bookshelf")
        bpy.context.scene.collection.children.link(bookshelf)

    if libr.gen_type == "SHELF" and libr.shelf_gen_type == "SINGLE":
        arr = [[{'x':0, 'z':0}]]
        createShelfBooks(ctx, arr, templates)
    elif libr.gen_type == "SHELF" and libr.shelf_gen_type == "STACK":
        raise Exception("Add STACK gen typ")
    elif libr.gen_type == "LIBRARY" and libr.library_gen_type == "GRID":
        arr = createGridArray(ctx)
        createShelfBooks(ctx, arr, templates)
    elif libr.gen_type == "LIBRARY" and libr.library_gen_type == "OBJECT":
        raise Exception("Add OJBECT gen type")
    else:
        self.report({"ERROR"}, "Mode not supported yet")

# Loop over array and fill up each shelf
def createShelfBooks(ctx, arr, template_collection):
    for row in arr:
        for obj in row:
            fillShelf(ctx, template_collection, obj)

def fillShelf(ctx, template_collection, obj):
    scene = ctx.scene
    libr = scene.library

    shelf_width = libr.module_width
    combined_width = 0
    previous_width = 0
    shelf_space = True
    rot = calcRotation(ctx)

    while shelf_space:
        if combined_width < shelf_width:
            copy = generateSingleBook(ctx, template_collection, obj)
            copy.location = (
                ((obj['x'] + ((previous_width / 2) + (copy.dimensions.x / 2)) + combined_width)),
                0,
                obj['z'],
            )
            copy.rotation_mode = "XYZ"
            copy.rotation_euler = (rot[0], rot[1], rot[2])
            combined_width += copy.dimensions.x + 0.008

            # Move new copy from starting collection to our Bookshelf collection
            bpy.data.collections[libr.books_collection].objects.unlink(copy)
            bpy.data.collections['Bookshelf'].objects.link(copy)
        else:
            shelf_space = False

def generateSingleBook(ctx, template_collection, obj):
    scene = ctx.scene
    libr = scene.library

    # Get random book from collection
    # This is my lazy way to make sure i dont run into index errors
    rNum = random.randint(0, len(template_collection.all_objects))
    while rNum == 0:
        rNum = random.randint(0, len(template_collection.all_objects))
    base = template_collection.all_objects[rNum - 1]

    bpy.ops.object.add_named(linked = False, name = base.name)
    copy = bpy.context.active_object

    # This is supposed to be for linked copies, but might remove all of it
    if libr.linked_copies:
        copy.data = base.data
    else:
        old = copy.data.name
        copy.data = base.data.copy()
        bpy.data.meshes.remove(bpy.data.meshes[old])

    # Set coords and apply scale/rot
    copy.location = (obj['x'], 0, obj['z'])
    scaling = calcBookDimensions(ctx)
    copy.scale[0] = scaling[0]
    copy.scale[1] = scaling[1]
    copy.scale[2] = scaling[2]
    bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)

    return copy

##########################################
# Math Helpers
##########################################

# Create an array of arrays for starting coordinates for each shelf
def createGridArray(ctx):
    scene = ctx.scene
    libr = scene.library

    shelf_arr = []
    for x in range(libr.shelf_rows):
        shelf_arr.append([])
        for y in range(libr.shelf_columns):
            shelf_arr[x].append(calcShelfCoords(ctx, x, y))
    
    return shelf_arr

# Calculte the starting coordinates for each shelf
# Returns x and z coords because we don't want to move on y axis at all
def calcShelfCoords(ctx, x, y):
    scene = ctx.scene
    libr = scene.library

    row_gap = libr.shelf_row_width
    col_gap = libr.shelf_column_width
    shelf_width = libr.module_width
    shelf_height = libr.module_height

    posX = x * (shelf_width + col_gap)
    posZ = y * (shelf_height + row_gap)

    return {'x': posX, 'z': posZ}

# Calculate book dimensions based on scaling variables
def calcBookDimensions(ctx):
    scene = ctx.scene
    libr = scene.library

    width_fac = libr.book_width_fac
    height_fac = libr.book_height_fac

    x = 1 + random.uniform(-0.7, 0.8) * width_fac
    y = 1
    z = 1 + random.uniform(-0.3, 0.6) * height_fac

    return (x, y, z)

# Calculate book rotation based on rotation variable
def calcRotation(ctx):
    scene = ctx.scene
    libr = scene.library

    rot_y = libr.book_rotY_fac
    rot_z = libr.book_rotZ_fac

    if libr.gen_type == "SHELF" and libr.shelf_gen_type == "STACK":
        z = random.uniform(-0.7, 0.7) * rot_z
        return (0, 0, z)
    else:
        y = random.uniform(-0.7, 0.7) * rot_y
        return (0, y, 0)
