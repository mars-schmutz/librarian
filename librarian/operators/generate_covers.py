import bpy
import bmesh
from bpy.props import *
from bpy.types import (Panel, Menu, Operator, PropertyGroup)

import random

class LIBR_OT_GenerateCovers(bpy.types.Operator):
    bl_idname = "libr.generate_covers"
    bl_label = "Generate Covers"
    bl_description = "Randomly generate covers."
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, ctx):
        scene = ctx.scene
        libr = scene.library

        # Get Blender user preferences and then find Librarian preferences
        # print(libr_prefs.title_dir)

        user_prefs = ctx.preferences
        libr_prefs = user_prefs.addons["librarian"].preferences

        try:
            booksCollection = bpy.data.collections['Bookshelf']
        except:
            booksCollection = None
            self.report({'ERROR'}, 'The Librarian collection hasn\'t been generated yet.')
            return { 'CANCELLED' }

        for i in booksCollection.objects:
            addMaterials(ctx, i)
        
        return { 'FINISHED' }

#########################################
# Material Helpers
#########################################

def addMaterials(ctx, obj):
    pass

#########################################
# Math Helpers
#########################################

def genRGB():
    return {"r": random.randint(0, 255), "g": random.randint(0, 255), "b": random.randint(0, 255)}
