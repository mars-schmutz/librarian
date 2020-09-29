import bpy
from bpy.props import StringProperty

class LibraryPreferences(bpy.types.AddonPreferences):
    bl_idname = 'librarian'

    collection_title: StringProperty(
            name = "Collection Title",
            description = "The name of the Collection to hold the generated books.",
            default = "Bookshelf"
    )

    title_dir: StringProperty(
            name = "Title Directory",
            description = "Directory containing title images.",
            default = "//",
            subtype = "DIR_PATH"
    )

    img_dir: StringProperty(
            name = "Image Directory",
            description = "Directory containing cover images.",
            default = "//",
            subtype = "DIR_PATH"
    )

    layout_dir: StringProperty(
            name = "Layout Directory",
            description = "Directory containing layout images.",
            default = "//",
            subtype = "DIR_PATH"
    )

    def draw(self, ctx):
        layout = self.layout
        box = layout.box()

        box.label(text = "Book Settings")
        box.prop(self, "collection_title")

        box = layout.box()
        box.label(text = "Cover Settings")
        box.prop(self, "title_dir")
        box.prop(self, "img_dir")
        box.prop(self, "layout_dir")
