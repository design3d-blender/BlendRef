#TEST SCRIPT

import bpy
import math
import json

selected = bpy.context.selected_objects

data = []

for i in selected:
    image = bpy.data.objects[i.name].data
    x = image.size[0]
    y = image.size[1]
    print(image.size[0],'x',image.size[1])
    if (x > y):
        y = (y*5)/x
        x = 5
    elif (x < y):
        x = (x*5)/y
        y = 5
    else:
        x = 5
        y = 5
    data.append(
        {'object': i.name,
        'x':x,
        'y':y,
        'image':image.name}
        )
    #data.append({i.name:[{'size':[{'x':image.size[0]},{'y':image.size[1]}]},{'sum':pseudoArea},{'image':image.name}]})

#print(data)

data.sort(key=lambda s: s['y'])
data.reverse()

test = []

for obj in data:
    test.append({'w':obj['x'], 'h':obj['y'],'name':obj['object']})

#test = [{'w':300, 'h':360}, {'w':250, 'h':250}, {'w':250, 'h':160}]

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


boxes = packer(test)

print(json.dumps(boxes,indent=2))
    
