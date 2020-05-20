import bpy
import os.path
from bpy.types import Operator

class BlendRef_OT_add_new_panel(Operator):
    bl_idname = 'ref.add_new_panel'
    bl_label = "Add a new Reference Panel"

    def execute(self, context):
        templatePath = os.path.dirname(os.path.realpath(__file__)) + '/template.blend'
        bpy.ops.workspace.append_activate(
            idname="Reference", #TODO change to property name
            filepath=templatePath)
        
        #this is an awful way to do this
        for area in bpy.data.workspaces['Reference'].screens[0].areas: #TODO change to property name
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    space.show_region_header = False
        return {'FINISHED'}

# classes = [
#     BlendRef_OT_add_new_panel,
# ]

# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls),

# def unregister():
#     for cls in classes:
#         bpy.utils.unregister_class(cls),

