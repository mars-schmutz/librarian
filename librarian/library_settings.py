import bpy
from bpy.props import StringProperty

class LibraryPreferences(bpy.types.AddonPreferences):
    bl_idname = 'librarian'

    title_dir = StringProperty(
            name = "Title Directory",
            description = "Directory containing title images.",
            default = "//",
            subtype = "DIR_PATH"
    )

    img_dir = StringProperty(
            name = "Image Directory",
            description = "Directory containing cover images.",
            default = "//",
            subtype = "DIR_PATH"
    )

    layout_dir = StringProperty(
            name = "Layout Directory",
            description = "Directory containing layout images.",
            default = "//",
            subtype = "DIR_PATH"
    )

    def draw(self, ctx):
        layout = self.layout

        layout.prop(self, "title_dir")
        layout.prop(self, "img_dir")
        layout.prop(self, "layout_dir")
