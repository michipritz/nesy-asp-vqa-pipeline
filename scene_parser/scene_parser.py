import json
import re

import torch

from pytorchyolo import models
from pytorchyolo.detect import detect
from pytorchyolo.utils.utils import rescale_boxes, to_cpu
from utils import PostprocessingMethod


class SceneParser:
    def __init__(self, config, weights, images, img_size, facts_out, conf_thres,
                 nms_thres, sd_factor, fallback_value, postprocessing_method):
        self.images = images
        self.config = config
        self.weights = weights
        self.img_size = img_size
        self.facts_out = facts_out
        self.conf_thres = conf_thres
        self.nms_thres = nms_thres
        self.sd_factor = sd_factor
        self.fallback_value = fallback_value
        self.postprocessing_method = postprocessing_method
        self.conf_mean = 0
        self.conf_sd = 0
        self.model = models.load_model(config, weights)

    def parse(self, data):
        # Make predictions for data
        predictions, _ = detect(self.model, data, self.conf_thres, self.nms_thres, self.postprocessing_method)

        # Calculate confidence mean and standard deviation based on the predictions for data
        if self.postprocessing_method == PostprocessingMethod.enhanced:
            self.conf_mean, self.conf_sd = _get_confidence_mean_and_sd(predictions)

        asp_facts = {}

        # Get ASP facts for every scene in data
        for scene_id, scene_predictions in enumerate(predictions):
            asp_facts[str(scene_id)] = []

            # Predicted boxes must be rescaled since the original images where rescaled by network before detection
            scene_predictions = rescale_boxes(scene_predictions, 480, (320, 480))

            # Move predictions from gpu to cpu and transform tensors in numpy array
            scene_predictions = to_cpu(scene_predictions).numpy()

            # Get ASP fact for every prediction within a scene
            for obj_id, prediction in enumerate(scene_predictions):
                fact = self.prediction_to_asp_fact(obj_id, prediction)
                asp_facts[str(scene_id)].append(fact)

        return asp_facts, self.conf_mean, self.conf_sd

    def prediction_to_asp_fact(self, obj_id, prediction):
        # Get rounded coordinates of bounding box prediction (Must be integers for ASP)
        x1 = round(prediction[0])
        y1 = round(prediction[1])
        x2 = round(prediction[2])
        y2 = round(prediction[3])

        if self.postprocessing_method == PostprocessingMethod.enhanced:
            fact = ''
            constraints = ''
            cls_probabilities = prediction[4:]

            for i, i_prob in enumerate(cls_probabilities):
                # Check whether class probability is above threshold
                if i_prob < self.conf_mean - self.sd_factor * self.conf_sd:
                    continue

                size, color, material, shape = _decode_category_id(i)

                tmp = f'obj({obj_id},{shape},{size},{color},{material},{x1},{y1},{x2},{y2});'
                fact += tmp
                constraints += f':~ {tmp[:-1]}. [{round(((1 - i_prob) + 1) * 1000)}]\n'

            # If no class probability exceeded the threshold the fallback_value highest scoring classes are chosen
            if not fact:
                fallback = sorted(range(len(cls_probabilities)), key=lambda cls_i: cls_probabilities[cls_i], reverse=True)[:self.fallback_value]
                for i in fallback:
                    size, color, material, shape = _decode_category_id(i)

                    tmp = f'obj({obj_id},{shape},{size},{color},{material},{x1},{y1},{x2},{y2});'
                    fact += tmp
                    constraints += f':~ {tmp[:-1]}. [{round(((1 - cls_probabilities[i]) + 1) * 1000)}]\n'

            return (
                f'{{{fact[:-1]}}} = 1.\n'
                f'{constraints}\n'
            )
        else:
            size, color, material, shape = _decode_category_id(prediction[5])
            return f'obj({obj_id},{shape},{size},{color},{material},{x1},{y1},{x2},{y2}).'


def _decode_category_id(category_id):
    with open('scene_parser/mappings/id_to_category.json', 'r') as mapping_file:
        category_str = json.load(mapping_file)[str(int(category_id))]

    properties_s = re.findall('[A-Z][^A-Z]*', category_str)

    size_s = properties_s[0]
    color_s = properties_s[1]
    material_s = properties_s[2]
    shape_s = properties_s[3]

    with open('scene_parser/mappings/properties_short_to_long.json', 'r') as mapping_file:
        properties_mapping = json.load(mapping_file)
        size_l = properties_mapping['sizes'][size_s]
        color_l = properties_mapping['colors'][color_s]
        material_l = properties_mapping['materials'][material_s]
        shape_l = properties_mapping['shapes'][shape_s]

    return size_l, color_l, material_l, shape_l


def _get_confidence_mean_and_sd(predictions):
    max_values = torch.Tensor()
    for prediction in predictions:
        prediction = to_cpu(prediction)
        max_values = torch.cat((max_values, torch.max(prediction[:, 4:], dim=1)[0]))

    return torch.mean(max_values).item(), torch.std(max_values).item()
