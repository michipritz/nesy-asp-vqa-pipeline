import os.path
import json
from pytorchyolo import detect, models
from scene_parser.utils.utils import predictions_to_asp_facts, get_confidence_mean_and_sd


# - Weight must be downloaded separately, due to big filesize.
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

        self.model = models.load_model(config, weights)

    def parse(self, data):
        if os.path.isfile(self.facts_out):
            with open(self.facts_out, 'r') as fp:
                asp_facts = json.load(fp)
        else:
            predictions, _ = detect.detect(
                self.model,
                data,
                self.conf_thres,
                self.nms_thres
            )

            asp_facts = predictions_to_asp_facts(predictions,
                                                 sd_factor=self.sd_factor,
                                                 backup_value=self.fallback_value,
                                                 standard_detection=self.postprocessing_method,
                                                 conf_threshold=self.conf_thres)

            with open(self.facts_out, 'w') as fp:
                asp_facts['info']['sd_factor'] = self.sd_factor
                asp_facts['info']['backup_value'] = self.fallback_value
                asp_facts['info']['img_size'] = self.img_size
                asp_facts['info']['conf_threshold_network'] = self.conf_thres
                asp_facts['info']['conf_threshold_parser'] = self.conf_thres
                asp_facts['info']['nms_threshold'] = self.nms_thres
                asp_facts['info']['data'] = self.images
                asp_facts['info']['weights'] = self.weights
                asp_facts['info']['config'] = self.config
                json.dump(asp_facts, fp, indent=4)

        return asp_facts
