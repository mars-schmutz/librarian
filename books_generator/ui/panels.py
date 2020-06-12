import bpy
from bpy.props import *
from bpy.types import (Panel, Menu, Operator, PropertyGroup, UIList)
import bpy.types

class OBJECT_PT_BooksGenerator(Panel):
    bl_idname = "object.book_wizard_PT_booksgen"
    bl_label = "Book Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Book Wizard"

    def draw(self, ctx):
        layout = self.layout
        scene = ctx.scene
        bw = scene.booksgen

        layout.operator('object.bw_generate', text = 'Generate').regen = False
        layout.operator('object.bw_generate', text = 'Regenerate').regen = True

        layout.prop(bw, "gen_seed")
        layout.prop(bw, "gen_type", expand = True)

        # Determine UI view based on gen_type value
        if bw.gen_type == "LIBRARY":
            layout.prop(bw, "library_gen_type", expand = True)

            # Determine UI view based on library_gen_type value
            if bw.library_gen_type == 'GRID':
                box = layout.box()
                box.label(text = 'Grid Settings')

                row = box.row()
                row.prop(bw, "shelf_rows")
                row.prop(bw, "shelf_columns")

                row = box.row()
                row.prop(bw, 'shelf_row_width')
                row.prop(bw, 'shelf_column_width')
            
            elif bw.library_gen_type == 'OBJECT':
                layout.label(text = 'Work on object gen type')
        
        elif bw.gen_type == 'SINGLE':
            layout.label(text = "Work on single gen")
        
        # General settings for all gen_types
        box = layout.box()
        box.label(text = 'General Settings')
        row = box.row()
        box.prop(bw, "books_limit")
        row = box.row()
        row.prop(bw, 'module_width')
        row.prop(bw, 'module_height')

        # Settings for variations in scaling
        box = layout.box()
        box.label(text = 'Scaling Settings')
        row = box.row()
        row.prop(bw, "book_width_fac")
        row.prop(bw, "book_height_fac")

        # Settings for variations in rotation
        box = layout.box()
        box.label(text = 'Rotation Settings')
        row = box.row()
        row.prop(bw, "book_rotY_fac")

class OBJECT_PT_BooksList(Panel):
    bl_idname = "object.book_wizard_PT_bookslist"
    bl_label = "Book List"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Book Wizard"

    def draw(self, ctx):
        layout = self.layout
        scene = ctx.scene
        bw = scene.booksgen

        layout.prop_search(bw, 'books_collection', bpy.data, 'collections')
        layout.prop(bw, 'linked_copies')