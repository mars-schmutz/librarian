# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Print to Info for logging
# self.report({'INFO'}, 'Printing report to Info window.')

bl_info = {
    "name": "Librarian",
    "author": "Mersh",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View",
    "description": "Easily generate shelves of books.",
    "warning": "This project is still under development. Save often and please use with caution.",
    "category": "3D View"
}

import bpy
import bmesh
import random
import bpy.utils.previews
import os
from mathutils import Vector, Matrix
from bpy.props import *
from bpy.types import (Panel,Menu,Operator,PropertyGroup)

# Addon Preferences
from . import library_settings

# Addon UI
from . ui.panels import LIBR_PT_BooksGenerator
from . ui.panels import LIBR_PT_BooksList
from . ui.panels import LIBR_PT_Covers

# Addon Operators
from . operators.generate_books import LIBR_OT_Generate
from . operators.generate_covers import LIBR_OT_GenerateCovers

# Global addon properties
class LIBRProperties(PropertyGroup):

    # General settings
    initial_gen: BoolProperty(
        name = 'Initial generation',
        description = 'Used to determine whether or not to display the Regenerate button',
        default = False
    )

    gen_type: EnumProperty(
        name = "Generation Type",
        items = (
            ("LIBRARY", "Library", "Generate a complete library"),
            ("SHELF", "Shelf", "Generate a single shelf of books"),
        ),
        description = "Determine the arrangement of books generated", default = "LIBRARY",
    )

    linked_copies: BoolProperty(
        name = "Linked Copies",
        description = "When active, books will be generated as linked copies of the base mesh",
        default = False,
    )

    books_collection: StringProperty(
        name = "Books Collection",
        description = "Collection of objects to use for book generation",
        default = "None",
    )

    # gen_type: Object settings
    library_object: StringProperty(
        name = "Library Object",
        description = "Object to act as the library shelf",
        default = "None",
    )

    # gen_type: Library settings
    library_gen_type: EnumProperty(
        name = "Library Gen Type",
        items = (
            ("GRID", "Grid", "Generate a library based on rows and columns"),
            ("OBJECT", "Object", "Generate a library based on detected shelves on the active object"),
        ),
        description = "Determine the type of Library generated",
        default = "GRID",
    )

    shelf_gen_type: EnumProperty(
        name = "Single Shelf Gen Type",
        items = (
            ("SINGLE", "Single Shelf", "Generate one shelf"),
            ("STACK", "Stack", "Generate a vertical stack of books"),
        ),
        description = "Determine the type of single shelf generated",
        default = "SINGLE",
    )

    # gen_type: Stack settings
    book_rotZ_fac: FloatProperty(
        name = "Z Variation",
        description = "Factor to control random Z axis rotation",
        min = 0,
        max = 1,
        default = 0,
    )

    # Library Grid rows and columns and width of each
    shelf_rows: IntProperty(
        name = "Columns",
        description = "Number of columns for library grid generation",
        min = 0,
        max = 50,
        default = 3,
    )

    shelf_columns: IntProperty(
        name = "Rows",
        description = "Number of rows for library grid generation",
        min = 0,
        max = 50,
        default = 3,
    )

    shelf_row_width: FloatProperty(
        name = "Row Width",
        description = "Width of each row gap for the library grid",
        min = 0,
        max = 50,
        default = 2,
    )

    shelf_column_width: FloatProperty(
        name = "Column Width",
        description = "Width of each column gap for the library grid",
        min = 0,
        max = 50,
        default = 2,
    )

    module_width: FloatProperty(
        name = "Module Width",
        description = "Width of each shelf module",
        min = 0,
        max = 50,
        default = 2
    )

    module_height: FloatProperty(
        name = "Module Height",
        description = "Height of each shelf module",
        min = 0,
        max = 50,
        default = 2
    )

    # Settings for each shelf module
    book_width_fac: FloatProperty(
        name = "Book Width Variation",
        description = "Variably adjust the scaling of the width of the book",
        min = 0,
        max = 1,
        default = 0
    )

    book_height_fac: FloatProperty(
        name = "Book Height Variation",
        description = "Variably adjust the scaling of the height of the book",
        min = 0,
        max = 1,
        default = 0
    )

    book_rotY_fac: FloatProperty(
        name = "Y Variation",
        description = "Variably adjust the rotation of each book on the Y axis",
        min = -1,
        max = 1,
        default = 0
    )

    cover_genre_fiction: BoolProperty(
        name = "Fiction",
        description = "Allow Librarian to generate covers for the fiction genre",
        default = True
    )

    cover_genre_nonfic: BoolProperty(
        name = "Non Fiction",
        description = "Allow Librarian to generate covers for the non fiction genre",
        default = False
    )

    cover_genre_textbook: BoolProperty(
        name = "Textbooks",
        description = "Allow Librarian to generate covers for textbooks",
        default = False
    )

    cover_genre_magazine: BoolProperty(
        name = "Magazine",
        description = "Allow Librarian to generate covers for magazines",
        default = False
    )

# Registration
classes = (

    # Addon Preferences
    library_settings.LibraryPreferences,

    # Properties group
    LIBRProperties,

    # Operators
    LIBR_OT_Generate,
    LIBR_OT_GenerateCovers,

    # Panels
    LIBR_PT_BooksGenerator,
    LIBR_PT_BooksList,
    LIBR_PT_Covers,
)

def register():
    from bpy.utils import register_class
    for c in classes:
        register_class(c)
    
    bpy.types.Scene.library = PointerProperty(type = LIBRProperties)
    # bpy.types.Scene.bookslist = CollectionProperty(type = BWList)
    bpy.types.Scene.list_index = IntProperty()

def unregister():
    from bpy.utils import unregister_class
    for c in reversed(classes):
        unregister_class(c)
    
    del bpy.types.Scene.booksgen
    del bpy.types.Scene.bookslist
    del bpy.types.Scene.list_index

if __name__ == "__main__":
    register()
