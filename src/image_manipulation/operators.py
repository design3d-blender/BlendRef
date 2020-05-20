import bpy
import os.path
import math
import json
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator, OperatorFileListElement

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

class BlendRef_OT_arrange_images(bpy.types.Operator):
    bl_idname = 'ref.arrange_images'
    bl_label = "Arrange images automatically"

    def execute(self,context):
        selected = bpy.context.selected_objects

        data = []

        margin = 0.5
        for i in selected:
            object = bpy.data.objects[i.name]
            image = object.data
            size = object.empty_display_size
            x = image.size[0]
            y = image.size[1]
            print(image.size[0],'x',image.size[1])
            if (x > y):
                y = (y*size)/x + margin
                x = size + margin
            elif (x < y):
                x = (x*size)/y + margin
                y = size + margin
            else:
                x = size + margin
                y = size + margin
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