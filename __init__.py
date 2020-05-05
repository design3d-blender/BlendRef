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
import os.path
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator, OperatorFileListElement

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

class BlendRef_OT_add_new_panel(bpy.types.Operator):
    bl_idname = 'ref.add_new_panel'
    bl_label = "Add a new Reference Panel"

    def execute(self, context):
        templatePath = os.path.dirname(os.path.realpath(__file__)) + '/resources/template.blend'
        bpy.ops.workspace.append_activate(
            idname="Reference", #TODO change to property name
            filepath=templatePath)
        
        #this is an awful way to do this
        for area in bpy.data.workspaces['Reference'].screens[0].areas: #TODO change to property name
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    space.show_region_header = False
        return {'FINISHED'}

class BlendRef_PT_AddPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BlendRef'
    bl_label = '1. Start Interface'

    def draw(self, context):
        self.layout.operator('ref.add_new_panel', text='Create Reference Panel', icon='MONKEY'),

class BlendRef_OT_add_images(bpy.types.Operator, ImportHelper):
    bl_idname = 'ref.add_images'
    bl_label = "Add a new Reference Panel"

    files = CollectionProperty(
            name="File Path",
            type=OperatorFileListElement,
            )
    directory = StringProperty(
            subtype='DIR_PATH',
            )

    filename_ext = ""

    def execute(self,context):
        colName = 'BlendRef'
        if (colName not in bpy.data.collections.keys()):
            collection = bpy.data.collections.new(colName)
            bpy.context.scene.collection.children.link(collection)
            bpy.data.collections[colName].hide_render = True
        import os
        directory = self.directory
        for file_elem in self.files:
            filepath = os.path.join(directory, file_elem.name)
            bpy.ops.object.load_reference_image(filepath = filepath)
            print(filepath)

        return{'FINISHED'}
        
        

class BlendRef_PT_LoadImages(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BlendRef'
    bl_label = '2. Load References'

    def draw(self, context):
        self.layout.operator('ref.add_images', text='Add Images', icon='FILEBROWSER'),

classes = [
    BlendRef_OT_add_new_panel,
    BlendRef_OT_add_images,
    BlendRef_PT_AddPanel,
    BlendRef_PT_LoadImages,

]

def register():
    for cls in classes:
        bpy.utils.register_class(cls),

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls),

