import argparse
import json

import numpy as np

if __name__ == '__main__':
    # Command line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='Path to the .json file containing the deterministic scene encoding')
    args = parser.parse_args()
    print(f'Command line arguments: {args}')

    out = []

    with open('data/CLEVR_v1.0/scenes/CLEVR_val_scenes.json', 'r') as fp:
        scenes_gt = json.load(fp)['scenes']

    with open(f'{args.input}', 'r') as fp:
        scene_encoding = json.load(fp)['facts']

    tp_global = 0  # True positives
    fp_global = 0  # False positives
    fn_global = 0  # False negatives
    gt_global = 0  # Ground truth detections
    shape_incorrect = 0  # Number of incorrectly predicted shapes
    size_incorrect = 0  # Number of incorrectly predicted sizes
    color_incorrect = 0  # Number of incorrectly predicted colors
    material_incorrect = 0  # Number of incorrectly predicted materials
    single_incorrect = 0  # Number of predictions for which a single attribute was falsely predicted
    double_incorrect = 0  # Number of predictions for which two attributes were falsely predicted
    triple_incorrect = 0  # Number of predictions for which three attributes were falsely predicted
    quadruple_incorrect = 0  # Number of predictions for which four attributes were falsely predicted

    for i, scene in enumerate(scenes_gt):  # iterate over scenes
        tp_local = 0
        fp_local = 0
        fn_local = 0
        gt_local = 0
        for j, obj_gt in enumerate(scene['objects']):  # iterate over objects in scene (ground truth)
            size_gt = obj_gt['size']
            color_gt = obj_gt['color']
            material_gt = obj_gt['material']
            shape_gt = obj_gt['shape']
            x_gt = obj_gt['pixel_coords'][0]
            y_gt = obj_gt['pixel_coords'][1]
            center_gt = np.array((x_gt, y_gt))

            gt_local += 1

            for obj_pred in scene_encoding[str(i)]:  # iterate over predicted objects for scene i
                _, _, size, color, material, shape, x1, y1, x2, y2 = obj_pred[4:-2].split(',')
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                x_pred = x1 + ((x2 - x1) / 2)
                y_pred = y2 + ((y1 - y2) / 2)
                center_pred = np.array((x_pred, y_pred))
                if np.linalg.norm(center_pred - center_gt) < 9:
                    if size == size_gt and color == color_gt and material == material_gt and shape == shape_gt:
                        tp_local += 1
                        break
                    else:
                        attr_incorrect = 0
                        if size != size_gt:
                            size_incorrect += 1
                            attr_incorrect += 1
                        if color != color_gt:
                            color_incorrect += 1
                            attr_incorrect += 1
                        if material != material_gt:
                            material_incorrect += 1
                            attr_incorrect += 1
                        if shape != shape_gt:
                            shape_incorrect += 1
                            attr_incorrect += 1

                        if attr_incorrect == 1:
                            single_incorrect += 1
                        elif attr_incorrect == 2:
                            double_incorrect += 1
                        elif attr_incorrect == 3:
                            triple_incorrect += 1
                        elif attr_incorrect == 4:
                            quadruple_incorrect += 1

        fp_local = len(scene_encoding[str(i)]) - tp_local
        fn_local = gt_local - tp_local

        tp_global += tp_local
        fp_global += fp_local
        fn_global += fn_local
        gt_global += gt_local

    out.append(f"Evaluation results for {args.input}")
    out.append(f"True positive: {tp_global}")
    out.append(f"False positive: {fp_global}")
    out.append(f"False negative: {fn_global}")
    out.append(f"Accuracy: {(tp_global / (tp_global + fn_global) * 100):.2f}")
    out.append(f"Precision: {(tp_global / (tp_global + fp_global) * 100):.2f}")
    out.append(f"Size incorrect: {size_incorrect}")
    out.append(f"Shape incorrect: {shape_incorrect}")
    out.append(f"Material incorrect: {material_incorrect}")
    out.append(f"Color incorrect: {color_incorrect}")
    out.append(f"Single error: {single_incorrect}")
    out.append(f"Double error: {double_incorrect}")
    out.append(f"Triple error: {triple_incorrect}")
    out.append(f"Quadruple error: {quadruple_incorrect}\n")

    print("\n".join(out))
