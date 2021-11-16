import json
import numpy as np

if __name__ == '__main__':
    out = []

    with open('data/CLEVR_v1.0/scenes/CLEVR_val_scenes.json', 'r') as fp:
        facts_gt = json.load(fp)['scenes']

    for epoch_idx, epoch in enumerate([25, 50, 200]):
        for conf in 25, 50:

            with open(f'results/facts_enhanced/facts_enhanced_{epoch}_conf{conf}.json', 'r') as fp:
                facts_pred = json.load(fp)['facts']

            tp_global = 0  # True positives
            fp_global = 0  # False positives
            fn_global = 0  # False negatives
            gt_global = 0  # Ground truth detections
            predictions_global = 0  # Total number of predictions

            for i, scene in enumerate(facts_gt):  # iterate over scenes
                tp_local = 0
                fp_local = 0
                fn_local = 0
                gt_local = 0

                ground_truth = set()

                for j, obj_gt in enumerate(scene['objects']):  # iterate over objects in scene (ground truth)
                    size_gt = obj_gt['size']
                    color_gt = obj_gt['color']
                    material_gt = obj_gt['material']
                    shape_gt = obj_gt['shape']
                    x_gt = obj_gt['pixel_coords'][0]
                    y_gt = obj_gt['pixel_coords'][1]
                    center_gt = tuple((x_gt, y_gt))

                    ground_truth.add((size_gt, color_gt, material_gt, shape_gt, center_gt))

                gt_global += len(ground_truth)
                predictions_global += len(facts_pred[str(i)])

                for disjunction in facts_pred[str(i)]:  # iterate over predicted objects for scene i
                    match = False
                    weights_list = []

                    predictions = disjunction.split('\n', 1)[0][1:-6].split(';')

                    for gt in ground_truth:
                        for obj_pred in predictions:
                            _, _, size, color, material, shape, x1, y1, x2, y2 = obj_pred[4:-1].split(',')
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            x_pred = x1 + ((x2 - x1) / 2)
                            y_pred = y2 + ((y1 - y2) / 2)
                            center_pred = np.array((x_pred, y_pred))
                            if np.linalg.norm(center_pred - np.array((gt[4][0], gt[4][1]))) < 9:
                                if size == gt[0] and color == gt[1] and material == gt[2] and shape == gt[3]:
                                    tp_global += 1
                                    match = True
                                    ground_truth.remove(gt)
                                    break
                        if match:
                            break

            fp_global = predictions_global - tp_global
            fn_global = gt_global - tp_global

            out.append(f"Evaluation stats for YOLOv3 ({epoch} Epochs, {conf / 100} Confidence threshold)")
            out.append(f"True positive: {tp_global}")
            out.append(f"False positive: {fp_global}")
            out.append(f"False negative: {fn_global}")
            out.append(f"Accuracy: {(tp_global/(tp_global+fn_global) * 100):.2f}")
            out.append(f"Precision: {(tp_global / (tp_global + fp_global) * 100):.2f}\n")

    with open("results/analysis_facts_enhanced.txt", "w") as fp:
        fp.write("\n".join(out))
