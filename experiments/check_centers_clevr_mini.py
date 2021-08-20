import json
import re
import numpy as np

if __name__ == "__main__":
    with open("data/clevr_mini/CLEVR_mini_coco_anns.json", "r") as fp:
        facts_gt = json.load(fp)["scenes"]

    with open("scene_parser/mappings/properties_short_to_long.json", "r") as fp:
        props_stl = json.load(fp)

    with open("scene_parser/mappings/id_to_category.json") as fp:
        id_to_cat = json.load(fp)

    deltas = []
    total_objs = 0

    for i, scene in enumerate(facts_gt):  # iterate over scenes
        with open(f"data/clevr_mini/labels/CLEVR_mini_{scene['image_index']:06d}.txt", "r") as fp:
            objs = []
            for line in fp:
                category_id, x, y = line.split(" ")[0:3]
                x, y = int(float(x) * 480), int(float(y) * 320)
                size, color, material, shape = re.findall("[A-Z][^A-Z]*", id_to_cat[category_id])
                size = props_stl["sizes"][size]
                color = props_stl["colors"][color]
                material = props_stl["materials"][material]
                shape = props_stl["shapes"][shape]
                objs.append((size, color, material, shape, np.array((x, y))))

            assert len(scene["objects"]) == len(objs)

            for obj_gt in scene['objects']:  # iterate over objects in scene (ground truth)
                size_gt = obj_gt['size']
                color_gt = obj_gt['color']
                material_gt = obj_gt['material']
                shape_gt = obj_gt['shape']
                x_gt = obj_gt['pixel_coords'][0]
                y_gt = obj_gt['pixel_coords'][1]
                center_gt1 = np.array((x_gt, y_gt))

                total_objs += 1

                for obj in objs:
                    if size_gt == obj[0] and color_gt == obj[1] and material_gt == obj[2] and shape_gt == obj[3]:
                        delta = np.linalg.norm(center_gt1 - obj[4])
                        if delta < 9:
                            deltas.append(delta)
                            break

    assert total_objs == len(deltas)
    print(max(deltas))
   