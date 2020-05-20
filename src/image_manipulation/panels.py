import bpy

class BlendRef_PT_LoadImages(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BlendRef'
    bl_label = '2. Load References'

    def draw(self, context):
        self.layout.operator('ref.add_images', text='Add Images', icon='FILEBROWSER'),
        self.layout.operator('ref.arrange_images', text='Arrange Images', icon='SNAP_VERTEX')
