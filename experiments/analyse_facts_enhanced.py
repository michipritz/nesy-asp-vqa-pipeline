import json
import numpy as np

if __name__ == '__main__':
    with open('data/CLEVR_v1.0/scenes/CLEVR_val_scenes.json', 'r') as fp:
        facts_gt = json.load(fp)['scenes']

    for epoch_idx, epoch in enumerate([50, 125, 200]):
        for conf in 25, 50:

            with open(f'facts_enhanced_new/facts_enhanced_{epoch}_conf{conf}.json', 'r') as fp:
                facts_pred = json.load(fp)['facts']

            tp_global = 0  # True positives
            fp_global = 0  # False positives
            fn_global = 0  # False negatives
            gt_global = 0  # Ground truth detections

            for i, scene in enumerate(facts_gt):  # iterate over scenes
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

                    for disjunction in facts_pred[str(i)]:  # iterate over predicted objects for scene i
                        match = False
                        weights_list = []

                        predictions = disjunction.split('\n', 1)[0][1:-6].split(';')

                        for obj_pred in predictions:
                            _, _, size, color, material, shape, x1, y1, x2, y2 = obj_pred[4:-1].split(',')
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            x_pred = x1 + ((x2 - x1) / 2)
                            y_pred = y2 + ((y1 - y2) / 2)
                            center_pred = np.array((x_pred, y_pred))
                            if np.linalg.norm(center_pred - center_gt) < 9:
                                if size == size_gt and color == color_gt and material == material_gt and shape == shape_gt:
                                    tp_local += 1
                                    math = True
                                    break
                        if match:
                            break

                fp_local = len(facts_pred[str(i)]) - tp_local
                fn_local = gt_local - tp_local

                tp_global += tp_local
                fp_global += fp_local
                fn_global += fn_local
                gt_global += gt_local

            print(f"Evaluation stats for YOLOv3 ({epoch} Epochs, {conf / 100} Confidence threshold)")
            print(f"True positive: {tp_global}")
            print(f"False positive: {fp_global}")
            print(f"False negative: {fn_global}")
            print(f"Accuracy: {(tp_global/(tp_global+fn_global) * 100):.2f}")
            print(f"Precision: {(tp_global / (tp_global + fp_global) * 100):.2f}\n")
