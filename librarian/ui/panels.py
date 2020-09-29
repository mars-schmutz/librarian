import bpy
from bpy.props import *
from bpy.types import (Panel, Menu, Operator, PropertyGroup, UIList)
import bpy.types

class LIBR_PT_BooksGenerator(Panel):
    bl_idname = "LIBRARIAN_PT_booksgen"
    bl_label = "Book Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Librarian"

    def draw(self, ctx):
        layout = self.layout
        scene = ctx.scene
        libr = scene.library

        layout.operator('libr.generate', text = 'Generate').regen = False
        layout.operator('libr.generate', text = 'Regenerate').regen = True

        layout.prop(libr, "gen_seed")
        layout.prop(libr, "gen_type", expand = True)

        # Determine UI view based on gen_type value
        if libr.gen_type == "LIBRARY":
            layout.prop(libr, "library_gen_type", expand = True)

            # Determine UI view based on library_gen_type value
            if libr.library_gen_type == 'GRID':
                box = layout.box()
                box.label(text = 'Grid Settings', icon = "SETTINGS")

                row = box.row()
                row.prop(libr, "shelf_rows")
                row.prop(libr, "shelf_columns")

                row = box.row()
                row.prop(libr, 'shelf_row_width')
                row.prop(libr, 'shelf_column_width')
            
            elif libr.library_gen_type == 'OBJECT':
                box = layout.box()
                box.label(text = "Object Settings", icon = "SETTINGS")
                
                row = box.row()
                row.prop_search(libr, "library_object", bpy.data, "objects")
        
        elif libr.gen_type == 'SINGLE':
            layout.label(text = "Single Shelf Settings", icon = "SETTINGS")

        # General settings for all gen_types
        box = layout.box()
        box.label(text = 'General Settings')
        row = box.row()
        box.prop(libr, "books_limit")
        row = box.row()
        row.prop(libr, 'module_width')
        row.prop(libr, 'module_height')

        # Settings for variations in scaling
        box = layout.box()
        box.label(text = 'Scaling Settings')
        row = box.row()
        row.prop(libr, "book_width_fac")
        row.prop(libr, "book_height_fac")

        # Settings for variations in rotation
        box = layout.box()
        box.label(text = 'Rotation Settings')
        row = box.row()
        row.prop(libr, "book_rotY_fac")

class LIBR_PT_BooksList(Panel):
    bl_idname = "LIBR_PT_bookslist"
    bl_label = "Book List"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Librarian"

    def draw(self, ctx):
        layout = self.layout
        scene = ctx.scene
        libr = scene.library

        layout.prop_search(libr, 'books_collection', bpy.data, 'collections')
        # layout.prop(libr, 'linked_copies')

class LIBR_PT_Covers(Panel):
    bl_idname = "LIBR_PT_covers"
    bl_label = "Covers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Librarian"

    def draw(self, ctx):
        layout = self.layout
        scene = ctx.scene
        libr = scene.library
