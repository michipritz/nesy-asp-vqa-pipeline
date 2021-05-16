import json
import re
import torch
from pytorchyolo.utils.utils import rescale_boxes, to_cpu


def predictions_to_asp_facts(predictions, sd_factor=2, backup_value=2):
    conf_mean, conf_sd = get_confidence_mean_and_sd(predictions)
    asp_facts = {'info': {'conf_mean': conf_mean, 'conf_sd': conf_sd}}
    
    for scene_id, scene_predictions in enumerate(predictions):
        asp_facts[str(scene_id)] = []
        scene_predictions = rescale_boxes(scene_predictions, 480, (320, 480))
        scene_predictions = to_cpu(scene_predictions).numpy()
        for obj_id, prediction in enumerate(scene_predictions):
            asp_facts[str(scene_id)].append(
                __prediction_to_asp_fact(obj_id, prediction, conf_mean, conf_sd, sd_factor, backup_value))
    return asp_facts


def __prediction_to_asp_fact(obj_id, prediction, conf_mean, conf_sd, sd_factor=2, backup_value=2):
    x1 = round(prediction[0])
    y1 = round(prediction[1])
    x2 = round(prediction[2])
    y2 = round(prediction[3])

    asp_fact = ''
    class_probabilities = prediction[4:]

    max_values = []
    if max(class_probabilities) < (conf_mean - sd_factor * conf_sd):
        max_values = sorted(class_probabilities, reverse=True)[:backup_value]

    for i, i_prob in enumerate(class_probabilities):
        if i_prob < conf_mean - sd_factor * conf_sd and not (i_prob in max_values):
            continue

        size, color, material, shape = __decode_category_id(i)
        tmp = 'obj({id},{shape},{size},{color},{material},{x1},{y1},{x2},{y2});'
        asp_fact += tmp.format(id=obj_id,
                               shape=shape,
                               size=size,
                               color=color,
                               material=material,
                               x1=x1,
                               y1=y1,
                               x2=x2,
                               y2=y2)

    asp_fact = '{' + asp_fact[:-1] + '} = 1.'
    if asp_fact == '{} = 1.':
        return ''
    else:
        return asp_fact


def __decode_category_id(category_id):
    with open('./scene_parser/utils/id_to_category.json', 'r') as mapping_file:
        category_str = json.load(mapping_file)[str(int(category_id))]

    properties_s = re.findall('[A-Z][^A-Z]*', category_str)

    size_s = properties_s[0]
    color_s = properties_s[1]
    material_s = properties_s[2]
    shape_s = properties_s[3]

    with open('./scene_parser/utils/properties_short_to_long.json', 'r') as mapping_file:
        properties_mapping = json.load(mapping_file)
        size_l = properties_mapping['sizes'][size_s]
        color_l = properties_mapping['colors'][color_s]
        material_l = properties_mapping['materials'][material_s]
        shape_l = properties_mapping['shapes'][shape_s]

    return size_l, color_l, material_l, shape_l


def get_confidence_mean_and_sd(predictions):
    max_values = torch.Tensor().to(predictions[0].device)
    for prediction in predictions:
        max_values = torch.cat((max_values, torch.max(prediction[:, 4:], dim=1)[0]))

    return torch.mean(max_values).item(), torch.std(max_values).item()
