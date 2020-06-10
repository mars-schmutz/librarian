import bpy
import bmesh
from bpy.props import *
from bpy.types import (Panel, Menu, Operator, PropertyGroup)

import random

class BW_OT_Generate(bpy.types.Operator):
    bl_idname = "object.bw_generate"
    bl_label = "Generate"
    bl_description = "Generate books based on settings"
    bl_options = { 'REGISTER', 'UNDO' }

    regen: BoolProperty(name = "Regeneration", default = False)

    def execute(self, ctx):
        scene = ctx.scene
        bw = scene.booksgen

        collection_name = bw.books_collection
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
        #    for i in booksCollection.all_objects:
                # self.report({'INFO'}, i.name)
                # bpy.context.view_layer.objects.active = bpy.data.objects[i.name]

                # I don't even know why this is needed, but it is
                for obj in bpy.context.selected_objects:
                    obj.select_set(False)

                if not self.regen:
                    genBookGroups(ctx, booksCollection.all_objects)
                else:
                    regenerateBookGroups(ctx, booksCollection.all_objects)
                
        return { 'FINISHED' }

def genBookGroups(ctx, collection):
    scene = ctx.scene
    bw = scene.booksgen

    cols = bw.shelf_columns
    rows = bw.shelf_rows
    col_gap = bw.shelf_column_width
    row_gap = bw.shelf_row_width

    try:
        bookshelf = bpy.data.collections['Bookshelf']
    except:
        bookshelf = bpy.data.collections.new('Bookshelf')
        bpy.context.scene.collection.children.link(bookshelf)

    # Get object from book collection
    book = collection[0]

    arr = genModuleArray(ctx)
    print(arr)

    for row in arr:
        for obj in row:
            # bpy.ops.object.add_named(linked = False, name = book.name)
            # copy = bpy.context.active_object
            # copy.location = (obj['x'], 0, obj['y'])

            fillShelf(ctx, obj)
            previous = None
            shelf_room = True
            while shelf_room:
                if previous == None:
                    copy = genObj(ctx, book, obj)
                    previous = copy
                    copy.location = (obj['x'], 0, obj['y'])
                else:
                    copy = genObj(ctx, book, obj)
                    copy.location = ((obj['x'] + previous.scale[0]), 0, obj['y'])
                    previous = copy
                
                if (obj['x'] + previous.scale[0]) > bw.module_width:
                    shelf_room = False
                print((obj['x'] + previous.scale[0]))
                print(bw.module_width)

                bpy.data.collections['Bookshelf'].objects.link(copy)
    
    # Remove dupes from starting collection
    bpy.ops.collection.objects_remove(collection = bw.books_collection)

def genModuleArray(ctx):
    scene = ctx.scene
    bw = scene.booksgen

    moduleArr = []
    for x in range(bw.shelf_rows):
        moduleArr.append([])
        for y in range(bw.shelf_columns):
            moduleArr[x].append(calcModuleCoords(ctx, x, y))
    
    return(moduleArr)

def regenerateBookGroups(ctx, collection):
    # Get collection
    bookshelf = bpy.data.collections['Bookshelf']

    # make sure nothing gets accidentally added to the selection set to be deleted
    # bpy.context.scene.objects.active = None

    for i in bookshelf.all_objects:
        i.select_set(True)
    bpy.ops.object.delete()

    genBookGroups(ctx, collection)

########################################
# Object Helpers
########################################

def genObj(ctx, base, obj):
    # Base generator for each book object
    scene = ctx.scene
    bw = scene.booksgen

    # bpy.ops.mesh.primitive_cube_add()
    bpy.ops.object.add_named(linked = False, name = base.name)
    copy = bpy.context.active_object

    if bw.linked_copies:
        copy.data = base.data
    else:
        old = copy.data.name
        copy.data = base.data.copy()
        bpy.data.meshes.remove(bpy.data.meshes[old])

    # Set coords
    copy.location = (obj['x'], 0, obj['y'])

    # Set scale
    scaling = calcBookDimensions(ctx)
    copy.scale[0] = scaling[0]
    copy.scale[1] = scaling[1]
    copy.scale[2] = scaling[2]
    
    return copy

def fillShelf(ctx, obj):
    pass

########################################
# Math Helpers
########################################

def calcModuleCoords(ctx, x, y):
    # Calculate the starting coordinates for each module
    scene = ctx.scene
    bw = scene.booksgen

    row_gap = bw.shelf_row_width
    col_gap = bw.shelf_column_width
    module_width = bw.module_width
    module_height = bw.module_height

    posX = x * (module_width + col_gap)
    posY = y * (module_height + row_gap)

    return {'x': posX, 'y': posY}

def calcBookDimensions(ctx):
    # Calculate the book dimensions based on the scaling variable
    scene = ctx.scene
    bw = scene.booksgen

    module_width = bw.module_width
    module_height = bw.module_height
    width_fac = bw.book_width_fac
    height_fac = bw.book_height_fac

    x = 1 + random.uniform(-0.7, 0.8) * width_fac
    y = 1
    z = 1 + random.uniform(-0.3, 0.6) * height_fac

    return (x, y, z)