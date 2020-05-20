import bpy
import os.path
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator, OperatorFileListElement

class BlendRef_PT_AddPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BlendRef'
    bl_label = '1. Start Interface'

    def draw(self, context):
        self.layout.operator('ref.add_new_panel', text='Create Reference Panel', icon='MONKEY'),

# classes = [
#     BlendRef_PT_AddPanel,
# ]

# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls),

# def unregister():
#     for cls in classes:
#         bpy.utils.unregister_class(cls),