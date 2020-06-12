import bpy
import os.path
import math
import json
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator, OperatorFileListElement

# class WM_OT_add_images(bpy.types.Operator):
#     """Open the Add Cube Dialog box"""
#     bl_label = "Add Cube Dialog Box"
#     bl_idname = "ref.add_images"
   
#     colname = bpy.props.StringProperty(name= "Enter Name", default= "")
#     dropdown_box: EnumProperty(
#         items=(
#             ("A", "Ahh", "Tooltip for A"),
#             ("B", "Be", "Tooltip for B"),
#             ("C", "Ce", "Tooltip for C"),
#         ),
#         name="Description for the Elements",
#         default="A",
#         description="Tooltip for the Dropdownbox",
#     )
#     def execute(self, context):     
#         return {'FINISHED'}
   
#     def invoke(self, context, event):
#         return context.window_manager.invoke_props_dialog(self)
    
#     def draw(self, context):
#         layout = self.layout
#         props = context.scene.BlendRefProps
#         layout.prop(props, "nameboard")
#         layout.operator('ref.add_images_outside', text='Add Images', icon='FILEBROWSER'),


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
        boardName = context.scene.BlendRefProps.nameboard
        if context.scene.BlendRefProps.canvasChoices != 'Create New Canvas':
            boardName = context.scene.BlendRefProps.refGroups
        if not boardName:
            boardName = "Canvas"
        colName = 'BlendRef'
        if (colName not in bpy.data.collections.keys()):
            collection = bpy.data.collections.new(colName)
            bpy.context.scene.collection.children.link(collection)
            bpy.data.collections[colName].hide_render = True
        if (boardName not in bpy.data.collections.keys()):
            collection = bpy.data.collections.new(boardName)
            bpy.data.collections[colName].children.link(collection)
            bpy.data.collections[boardName].hide_render = True
        import os
        directory = self.directory
        for file_elem in self.files:
            filepath = os.path.join(directory, file_elem.name)
            scene = context.scene
            cursor = scene.cursor.location

            try:
                image = bpy.data.images.load(filepath, check_existing=True)
            except RuntimeError as ex:
                self.report({'ERROR'}, str(ex))
                return {'CANCELLED'}

            bpy.ops.object.empty_add(
                'INVOKE_REGION_WIN',
                type='IMAGE',
                location=cursor,
                align=('VIEW'),
            )

            view_layer = context.view_layer
            obj = view_layer.objects.active
            obj.data = image
            obj.name = image.name
            obj.empty_display_size = 5.0
            # Remove object from all collections not used in a scene
            bpy.ops.collection.objects_remove_all()
            # add it to our specific collection
            bpy.data.collections[boardName].objects.link(obj)
            print(filepath)

        return {'FINISHED'}

class BlendRef_OT_arrange_images(bpy.types.Operator):
    bl_idname = 'ref.arrange_images'
    bl_label = "Arrange images automatically"
    bl_options = {'REGISTER', 'UNDO'}

    margin: bpy.props.FloatProperty(
                name="Margin",
                description="Margin between auto-arranged images",
                min=0,
                max=10,
            )

    def execute(self,context):
        selected = bpy.context.selected_objects

        data = []

        for i in selected:
            object = bpy.data.objects[i.name]
            image = object.data
            size = object.empty_display_size
            scale_x = object.scale[0]
            scale_y = object.scale[1]
            x = image.size[0]
            y = image.size[1]
            if (x > y):
                y = ((y*size)/x)*scale_y + self.margin
                x = (size)*scale_x + self.margin
            elif (x < y):
                x = ((x*size)/y)*scale_x + self.margin
                y = (size)*scale_y + self.margin
            else:
                x = size*scale_x + self.margin
                y = size*scale_y + self.margin
            data.append(
                {'object': i.name,
                'x':x,
                'y':y,
                'image':image.name}
                )

        # sort the images from highest to lowest (in y axis)
        data.sort(key=lambda s: s['y'])
        data.reverse()

        images = []

        for obj in data:
            images.append({'w':obj['x'], 'h':obj['y'],'name':obj['object']})

        # Packer based (or probably stollen) from  mapbox/potpack
        # https://github.com/mapbox/potpack
        # In here a more datailed explanation for the algorithm 
        # https://observablehq.com/@mourner/simple-rectangle-packing
        def packer(boxes):
            area = 0
            maxW = 0
            for box in boxes:
                area += box['w'] * box['h']
                maxW = max(maxW, box['w'])
            
            startW = max(math.ceil(math.sqrt(area/0.95)), maxW)
            spaces = [{'x':0, 'y':0, 'w': startW, 'h': math.inf}]
            packed = []

            for box in boxes:
                i = len(spaces)-1
                while i >= 0:
                    i -= 1
                    space = spaces[i]
                    if (box['w'] > space['w'] or box['h'] > space['h']):
                        continue

                    packed.append({'object':box['name'],'w':box['w'],'h':box['h'],'x':space['x'],'y':space['y']})

                    if (box['w'] == space['w'] and box['h'] == space['h']):
                        last = spaces.pop()
                        if (i < len(spaces)):
                            spaces[i] = last
                    elif (box['h'] == space['h']):
                            space['x'] += box['w']
                            space['w'] -= box['w']
                    elif (box['w'] == space['w']):
                        space['y'] += box['h']
                        space['h'] -= box['h']
                    else:
                        spaces.append({
                                    'x':space['x'] + box['w'],
                                    'y':space['y'],
                                    'w':space['w'] - box['w'],
                                    'h':box['h']})
                        space['y'] += box['h']
                        space['h'] -= box['h']
                    break
            return packed


        packedImages = packer(images)

        #print(json.dumps(boxes,indent=2))
        
        #locate each image on its corresponding place in the calculated grid
        for obj in packedImages:
            image = bpy.data.objects[obj['object']]
            image.location[0] = obj['x'] + obj['w']/2
            image.location[2] = -obj['y'] - obj['h']/2
            #adjust origin point if image is resized
            image.empty_image_offset[0] = -0.5
            image.empty_image_offset[1] = -0.5
        
        #select all images and align
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.view3d.view_selected(use_all_regions=False)
        return{'FINISHED'}      