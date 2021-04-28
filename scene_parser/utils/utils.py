import json
import re


def predictions_to_asp_facts(predictions):
    asp_facts = []
    for obj_id, prediction in enumerate(predictions):
        asp_facts.append(__prediction_to_asp_fact(obj_id, prediction))
    return asp_facts


def __prediction_to_asp_fact(obj_id, prediction):
    x1 = round(prediction[0])
    y1 = round(prediction[1])
    x2 = round(prediction[2])
    y2 = round(prediction[3])
    size, color, material, shape = __decode_category_id(prediction[5])
    asp_fact = 'obj({id},{shape},{size},{color},{material},{x1},{y1},{x2},{y2}).'
    return asp_fact.format(id=obj_id,
                           shape=shape,
                           size=size,
                           color=color,
                           material=material,
                           x1=x1,
                           y1=y1,
                           x2=x2,
                           y2=y2)


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
