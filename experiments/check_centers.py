import json
import numpy as np

if __name__ == '__main__':
    with open('../data/CLEVR_v1.0/scenes/CLEVR_val_scenes.json', 'r') as fp:
        facts_gt = json.load(fp)['scenes']

    deltas = []
    total_objs = 0

    for i, scene in enumerate(facts_gt):  # iterate over scenes
        for j, obj_gt1 in enumerate(scene['objects']):  # iterate over objects in scene (ground truth)
            size_gt1 = obj_gt1['size']
            color_gt1 = obj_gt1['color']
            material_gt1 = obj_gt1['material']
            shape_gt1 = obj_gt1['shape']
            x_gt1 = obj_gt1['pixel_coords'][0]
            y_gt1 = obj_gt1['pixel_coords'][1]
            center_gt1 = np.array((x_gt1, y_gt1))

            total_objs += 1

            for k, obj_gt2 in enumerate(scene['objects']):  # iterate over objects in scene (ground truth)
                size_gt2 = obj_gt2['size']
                color_gt2 = obj_gt2['color']
                material_gt2 = obj_gt2['material']
                shape_gt2 = obj_gt2['shape']
                x_gt2 = obj_gt2['pixel_coords'][0]
                y_gt2 = obj_gt2['pixel_coords'][1]
                center_gt2 = np.array((x_gt2, y_gt2))

                delta = np.linalg.norm(center_gt1 - center_gt2)

                if k != j and delta < 18:
                    print(f"Obj 1: {size_gt1}, {color_gt1}, {material_gt1}, {shape_gt1}, {center_gt1}")
                    print(f"Obj 2: {size_gt2}, {color_gt2}, {material_gt2}, {shape_gt2}, {center_gt2}")
                    print(f"Distance: {delta}")
                    print("----")
                if k != j:
                    deltas.append(delta)

    print(min(deltas))
    print(total_objs)

