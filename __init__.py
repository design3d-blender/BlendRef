# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
from .src.ui.operators import BlendRef_OT_add_new_panel
from .src.ui.panels import BlendRef_PT_AddPanel
from .src.image_manipulation.operators import BlendRef_OT_add_images, BlendRef_OT_arrange_images
from .src.image_manipulation.panels import BlendRef_PT_LoadImages

bl_info = {
    "name" : "BlendRef",
    "author" : "design3D",
    "description" : "",
    "blender" : (2, 90, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "View3D"
}       

classes = [
    BlendRef_OT_add_new_panel,
    BlendRef_OT_add_images,
    BlendRef_OT_arrange_images,
    BlendRef_PT_AddPanel,
    BlendRef_PT_LoadImages,

]

def register():
    for cls in classes:
        bpy.utils.register_class(cls),

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls),

