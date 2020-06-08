import bpy
from bpy.props import *
from bpy.types import (Panel, Menu, Operator, PropertyGroup, UIList)
import bpy.types

class OBJECT_PT_LayoutTest(Panel):
    bl_idname = "object.book_wizard_layout_test"
    bl_label = "Example Layout Test"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Book Wizard"

    def draw(self, ctx):
        layout = self.layout
        scene = ctx.scene
        bw = scene.booksgen
        obj = ctx.object

        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")

        row = layout.row()
        row.operator("mesh.primitive_cube_add")

        box = layout.box()
        box.label(text="Selection Tools")
        box.operator("object.select_all").action = 'TOGGLE'
        row = box.row()
        row.operator("object.select_all").action = 'INVERT'
        row.operator("object.select_random")

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
                box.prop(bw, "books_limit")

                row = box.row()
                row.prop(bw, "shelf_rows")
                row.prop(bw, "shelf_columns")

                row = box.row()
                row.prop(bw, 'shelf_row_width')
                row.prop(bw, 'shelf_column_width')

                row = box.row()
                row.prop(bw, 'module_width')
                row.prop(bw, 'module_height')
            
            elif bw.library_gen_type == 'OBJECT':
                layout.label(text = 'Work on object gen type')
        
        elif bw.gen_type == 'SINGLE':
            layout.label(text = "Work on single gen")

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