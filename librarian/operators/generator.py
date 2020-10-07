import bpy
import bmesh
from bpy.props import *
from bpy.types import (Panel, Menu, Operator, PropertyGroup)

import random
import time

########################################
# Operator Classes
########################################

class LIBR_OT_Generate(bpy.types.Operator):
    bl_idname = "libr.generate"
    bl_label = "Generate" 
    bl_description = "Generate books based on settings."
    bl_options = { 'REGISTER', 'UNDO' }

    regen: BoolProperty(name = "Regeneration", default = False)

    def execute(self, ctx):
        scene = ctx.scene
        libr = scene.library

        collection_name = libr.books_collection
        try:
            booksCollection = bpy.data.collections[collection_name]
        except:
            booksCollection = None
            self.report({'ERROR'}, 'Select the books collection.')
            return { 'CANCELLED' }

        if booksCollection is None:
            self.report({'ERROR'}, 'Select the books collection.')
            return { 'CANCELLED' }
        else:
            # I don't even know why this is needed, but it is
            for obj in bpy.context.selected_objects:
                obj.select_set(False)

            tStart = time.time()
            if not self.regen:
                genBookGroups(ctx, booksCollection)
            else:
                regenerateBookGroups(ctx, booksCollection)
            print("Generation time: {0}s".format(time.time() - tStart))
                
        return { 'FINISHED' }

class LIBR_OT_Import(bpy.types.Operator):
    bl_idname = "libr.import"
    bl_label = "Import"
    bl_description = "Easily import prebuilt book collection from helper file."
    bl_options = { "REGISTER", "UNDO" }

    def execute(self, ctx):
        scene = ctx.scene
        libr = scene.library
        user_prefs = ctx.preferences
        libr_prefs = user_prefs.addons["librarian"].preferences
        fName = libr_prefs.books_blend

########################################
# Object Helpers
########################################

def genBookGroups(ctx, booksCollection):
    scene = ctx.scene
    libr = scene.library

    cols = libr.shelf_columns
    rows = libr.shelf_rows
    col_gap = libr.shelf_column_width
    row_gap = libr.shelf_row_width

    try:
        bookshelf = bpy.data.collections['Bookshelf']
    except:
        bookshelf = bpy.data.collections.new('Bookshelf')
        bpy.context.scene.collection.children.link(bookshelf)

    if libr.gen_type == 'SINGLE':
        arr = [[{'x':0, 'y':0}]]
    elif libr.gen_type == 'LIBRARY' and libr.library_gen_type == 'GRID':
        arr = genModuleArray(ctx)
        # print(arr)
    elif libr.gen_type == "OBJECT":
        arr = genObjArray(ctx)
    else:
        print('Mode not supported yet')
    
    for row in arr:
        for obj in row:
            fillModule(ctx, booksCollection, obj)
            # bpy.data.collections['Bookshelf'].objects.link(copy)

def regenerateBookGroups(ctx, collection):
    # Get collection
    bookshelf = bpy.data.collections['Bookshelf']

    for i in bookshelf.all_objects:
        i.select_set(True)
    bpy.ops.object.delete()

    genBookGroups(ctx, collection)


def genModuleArray(ctx):
    # Generation for MODULE type
    scene = ctx.scene
    libr = scene.library

    moduleArr = []
    for x in range(libr.shelf_rows):
        moduleArr.append([])
        for y in range(libr.shelf_columns):
            moduleArr[x].append(calcModuleCoords(ctx, x, y))
    
    return(moduleArr)

def genObjArray(ctx):
    # Generation for the OBJECT type
    pass

def genObj(ctx, booksCollection, obj):
    # Base generator for each book object for the MODULE gen settings
    scene = ctx.scene
    libr = scene.library

    # Get random book from book collection
    rNum = random.randint(0, len(booksCollection.all_objects))
    while rNum == 0:
        rNum = random.randint(0, len(booksCollection.all_objects))
    base = booksCollection.all_objects[rNum - 1]

    bpy.ops.object.add_named(linked = False, name = base.name)
    copy = bpy.context.active_object

    if libr.linked_copies:
        copy.data = base.data
    else:
        old = copy.data.name
        copy.data = base.data.copy()
        bpy.data.meshes.remove(bpy.data.meshes[old])

    # Set coords
    copy.location = (obj['x'], 0, obj['y'])

    # Set and apply scale
    scaling = calcBookDimensions(ctx)
    copy.scale[0] = scaling[0]
    copy.scale[1] = scaling[1]
    copy.scale[2] = scaling[2]
    bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)

    # Remove dupes from starting collection
    # bpy.ops.collection.objects_remove(collection = bw.books_collection)

    return copy

def fillModule(ctx, booksCollection, obj):
    scene = ctx.scene
    libr = scene.library

    module_width = libr.module_width
    combined_width = 0
    previous_width = 0
    shelf_space = True
    rot = calcRotation(ctx)

    while shelf_space:
        if combined_width < module_width:
            copy = genObj(ctx, booksCollection, obj)
            copy.location = (
                ((obj['x'] + ((previous_width / 2) + (copy.dimensions.x / 2)) + combined_width)) + rot[0],
                0 + rot[1],
                obj['y'] + rot[2]
            )
            copy.rotation_mode = 'XYZ'
            copy.rotation_euler = (rot[0], rot[1], rot[2])
            combined_width += copy.dimensions.x + 0.008

            # Move new copy from starting collection to our new collection
            bpy.data.collections[libr.books_collection].objects.unlink(copy)
            bpy.data.collections['Bookshelf'].objects.link(copy)
        else:
            shelf_space = False

########################################
# Math Helpers
########################################

def calcModuleCoords(ctx, x, y):
    # Calculate the starting coordinates for each module
    # The Y coordinate here is equivalent to the Z coordinate in Blender's API
    # I'm not a smart man, so my dumbass was thinking of a 2D coordinate system while working on this function
    scene = ctx.scene
    libr = scene.library

    row_gap = libr.shelf_row_width
    col_gap = libr.shelf_column_width
    module_width = libr.module_width
    module_height = libr.module_height

    posX = x * (module_width + col_gap)
    posY = y * (module_height + row_gap)

    return {'x': posX, 'y': posY}

def calcBookDimensions(ctx):
    # Calculate the book dimensions based on the scaling variable
    scene = ctx.scene
    libr = scene.library

    width_fac = libr.book_width_fac
    height_fac = libr.book_height_fac

    x = 1 + random.uniform(-0.7, 0.8) * width_fac
    y = 1
    z = 1 + random.uniform(-0.3, 0.6) * height_fac

    return (x, y, z)

def calcRotation(ctx):
    scene = ctx.scene
    libr = scene.library

    rot_y = libr.book_rotY_fac

    x = 0
    y = random.uniform(-0.7, 0.7) * rot_y
    z = 0

    return (x, y, z)
