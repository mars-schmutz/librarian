import bpy
from bpy.props import *
from bpy.types import (Panel, Menu, Operator, PropertyGroup, UIList)
import bpy.types

class LIBR_PT_BooksImport(Panel):
    bl_idname = "LIBRARIAN_PT_import"
    bl_label = "Import Collection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Librarian"

    def draw(self, ctx):
        layout = self.layout
        scene = ctx.scene
        libr = scene.library
        user_prefs = ctx.preferences
        libr_prefs = user_prefs.addons["librarian"].preferences

        layout.operator('libr.import', text = "Import")

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
        
        elif libr.gen_type == 'SHELF':
            layout.prop(libr, "shelf_gen_type", expand = True)

            # Determin UI based on single_gen_type
            # We shouldn't need a separate if statement for 'SINGLE' becasue we don't have any settings specific to a single shelf
            if libr.single_gen_type == 'STACK':
                box = layout.box()
                box.label(text = "Stack Settings", icon = "SETTINGS")

                row = box.row()
                row.prop(libr, 'book_rotZ_fac')

        # General settings for all gen_types
        box = layout.box()
        box.label(text = 'General Settings')
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

        layout.operator("libr.generate_covers", text = "Generate")

        box = layout.box()
        box.label(text = "Cover Types")
        col = box.column()
        col.prop(libr, "cover_genre_fiction")
        col.prop(libr, "cover_genre_nonfic")
        col.prop(libr, "cover_genre_textbook")
        col.prop(libr, "cover_genre_magazine")
